import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, Response
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import date, timedelta
from typing import List
from dotenv import load_dotenv
from jose import JWTError, jwt
import traceback

# Load environment variables
load_dotenv()

# Models
from src.models.user import User
from src.models.caravan import Caravan
from src.models.review import Review
from src.models.poi import PointOfInterest
from src.models.reservation import Reservation, ReservationCreate
from src.models.schemas import UserCreate, ReservationDetails

# Data
from src.data.mock_pois import MOCK_POIS

# Repositories
from src.repositories.base_repository import BaseRepository
from src.repositories.reservation_repository import ReservationRepository
from src.repositories.user_repository import UserRepository

# Services
from src.services.reservation_service import ReservationService
from src.services.notification_service import NotificationService
from src.services.review_service import ReviewService
from src.services.recommendation_service import RecommendationService
from src.services.auth_service import AuthService

# Validators
from src.validators.reservation_validator import ReservationValidator

# Patterns
from src.patterns.strategies import LongStayDiscount

from fastapi.security import OAuth2PasswordRequestForm

# Security
from src.security import get_token_from_cookie

from fastapi.middleware.cors import CORSMiddleware

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow specific origin
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# --- 애플리케이션 초기화 ---
print("--- CaravanShare 애플리케이션 초기화 ---")

# 1. 핵심 서비스 및 저장소 인스턴스화 (전역)
user_repo = UserRepository()
app.state.user_repo = user_repo # Attach repo to app state for dependency injection

caravan_repo = BaseRepository[Caravan]()
reservation_repo = ReservationRepository()
review_repo = BaseRepository[Review]()
notification_service = NotificationService()
recommendation_service = RecommendationService(caravan_repo)
auth_service = AuthService(user_repo)
print("저장소 및 서비스 준비 완료.")

# 2. 초기 데이터 생성
host_user = user_repo.save(User(user_id=101, name="김호스트", email="host@example.com", balance=0))
another_host = user_repo.save(User(user_id=102, name="이호스트", email="host2@example.com", balance=0))

caravan_repo.save(Caravan(
    caravan_id=1, name="별밤지기 캠퍼", owner_id=host_user.user_id, type="Campervan", price_per_day=120.0,
    location="경기도 양평", sleeps=2, description="별보기 좋은 넓은 창을 가진 커플용 감성 캠퍼밴입니다. 로맨틱한 여행에 최적화되어 있습니다.",
    image_url="/images/Gemini_Generated_Image_arlr5aarlr5aarlr.png"
))
caravan_repo.save(Caravan(
    caravan_id=2, name="어드벤처 패밀리", owner_id=another_host.user_id, type="Motorhome", price_per_day=250.0,
    location="강원도 인제", sleeps=5, description="산과 계곡, 어디든 갈 수 있는 튼튼한 가족용 모터홈. 자전거 거치대와 루프탑 텐트가 포함되어 있습니다.",
    image_url="https://placehold.co/600x400/718096/FFFFFF?text=Adventure+Family"
))
caravan_repo.save(Caravan(
    caravan_id=3, name="럭셔리 글램퍼", owner_id=host_user.user_id, type="Trailer", price_per_day=350.0,
    location="제주도 애월", sleeps=4, description="호텔 스위트룸 부럽지 않은 최고급 시설을 갖춘 럭셔리 트레일러. 편안하고 프라이빗한 휴가를 즐겨보세요.",
    image_url="https://placehold.co/600x400/E2E8F0/2D3748?text=Luxury+Glamper"
))
print(f"새로운 테스트 데이터 3개 생성 완료.")

# 3. 비즈니스 로직 컴포넌트 인스턴스화 (의존성 주입)
validator = ReservationValidator(user_repo, caravan_repo, reservation_repo)
reservation_service = ReservationService(
    user_repo, caravan_repo, reservation_repo, validator, discount_strategy=LongStayDiscount()
)
review_service = ReviewService(review_repo, reservation_repo, caravan_repo)
print("모든 서비스 및 검증기 준비 완료.")


# --- Dependency for getting current user ---
async def get_current_user(token: str = Depends(get_token_from_cookie)) -> User:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, AuthService.SECRET_KEY, algorithms=[AuthService.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = app.state.user_repo.find_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user


# --- API 엔드포인트 정의 ---

@app.get("/")
def read_root():
    """루트 엔드포인트로, API 서버가 실행 중인지 확인합니다."""
    return {"message": "CaravanShare API 서버에 오신 것을 환영합니다!"}

# --- Auth Endpoints ---

@app.post("/api/auth/signup", response_model=User, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate):
    """
    Register a new user with email and password.
    """
    try:
        return auth_service.register_user(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/token")
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate with email/password, set HttpOnly cookie, and return a JWT.
    """
    user = auth_service.authenticate_user(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "user_id": user.user_id}
    )
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=False, # Should be True in production
        samesite="lax",
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/url/google")
def get_google_auth_url():
    """Google 로그인 페이지로 리디렉션할 URL을 반환합니다."""
    return {"url": auth_service.get_google_auth_url()}

@app.get("/api/auth/callback/google")
async def auth_callback_google(code: str):
    """Google 로그인 후 리디렉션되는 콜백 엔드포인트입니다."""
    try:
        jwt_token = await auth_service.handle_google_login(code)
        response = RedirectResponse(url="http://localhost:3000/")
        response.set_cookie(
            key="access_token",
            value=f"Bearer {jwt_token}",
            httponly=True,
            secure=False,
            samesite="lax",
        )
        return response
    except Exception as e:
        print(f"An error occurred during Google authentication: {e}")
        raise HTTPException(
            status_code=400,
            detail="Authentication failed. Please try again."
        )

@app.get("/api/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """현재 로그인된 사용자의 정보를 반환합니다."""
    return current_user

@app.get("/api/users/me/reservations", response_model=List[ReservationDetails])
def get_my_reservations(current_user: User = Depends(get_current_user)):
    """
    Returns all reservations for the current logged-in user with caravan details.
    """
    user_reservations = reservation_repo.find_by_user_id(current_user.user_id)
    
    response_data = []
    for res in user_reservations:
        caravan = caravan_repo.find_by_id(res.caravan_id)
        if caravan:
            details = ReservationDetails(
                reservation_id=res.reservation_id,
                start_date=res.start_date,
                end_date=res.end_date,
                total_price=res.total_price,
                status=res.status,
                caravan_name=caravan.name,
                caravan_image_url=caravan.image_url
            )
            response_data.append(details)
            
    return response_data

# --- Caravan and POI Endpoints ---

@app.get("/api/points-of-interest", response_model=List[PointOfInterest])
def get_points_of_interest(location: str):
    """
    Returns a list of points of interest (campgrounds, toilets) for a given location.
    """
    print(f"--- DEBUG: /api/points-of-interest called with location: {location} ---")
    pois = MOCK_POIS.get(location, [])
    print(f"--- DEBUG: Found {len(pois)} POIs for {location}. ---")
    return pois

@app.get("/api/caravans")
def get_caravans():
    """(DEBUGGING) Manually serializes the caravan list to JSON."""
    print("--- DEBUG: Testing manual JSON serialization ---")
    try:
        caravans = caravan_repo.find_all()
        print(f"--- DEBUG: Found {len(caravans)} caravans. Manually encoding... ---")
        json_compatible_caravans = jsonable_encoder(caravans)
        print("--- DEBUG: Manual encoding successful. Returning JSONResponse. ---")
        return JSONResponse(content=json_compatible_caravans)
    except Exception as e:
        print(f"--- DEBUG: An exception occurred during manual serialization: ---")
        traceback.print_exc()
        raise

@app.get("/api/caravans/{caravan_id}")
def get_caravan_by_id(caravan_id: int):
    """
    Returns a single caravan by its ID, with manual JSON encoding and error tracing.
    """
    print(f"--- DEBUG: /api/caravans/{caravan_id} called ---")
    try:
        caravan = caravan_repo.find_by_id(caravan_id)
        if not caravan:
            raise HTTPException(status_code=404, detail="Caravan not found")
        
        print(f"--- DEBUG: Found caravan '{caravan.name}'. Manually encoding... ---")
        json_compatible_caravan = jsonable_encoder(caravan)
        print("--- DEBUG: Manual encoding successful. Returning JSONResponse. ---")
        return JSONResponse(content=json_compatible_caravan)
    except Exception as e:
        print(f"--- DEBUG: An exception occurred in get_caravan_by_id for id {caravan_id}: ---")
        traceback.print_exc()
        raise

# --- Reservation Endpoints ---

@app.post("/api/reservations", response_model=Reservation, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation_data: ReservationCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Creates a new reservation for the current user.
    """
    # The reservation_service has detailed internal logging.
    # We need to add a balance to the user for testing purposes.
    if current_user.balance == 0:
        print(f"--- DEBUG: Adding 10000 to balance for user {current_user.user_id} for testing ---")
        current_user.balance = 10000

    new_reservation = reservation_service.create_reservation(
        user_id=current_user.user_id,
        caravan_id=reservation_data.caravan_id,
        start_date=reservation_data.start_date,
        end_date=reservation_data.end_date
    )
    
    if new_reservation is None:
        # The service layer handles logging the specific error.
        # We return a generic bad request error to the client.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reservation failed. Caravan may not be available, dates may be invalid, or funds may be insufficient."
        )
    return new_reservation

if __name__ == "__main__":
    """Uvicorn을 사용하여 FastAPI 애플리케이션을 실행합니다."""
    print("--- API 서버 시작 ---")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)