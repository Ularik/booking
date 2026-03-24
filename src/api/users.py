from fastapi import APIRouter, HTTPException, Response
from src.schemas.users import UsersRequestSchema, UserAddSchema, UserLoginSchema
from src.repositories.users import UsersRepository
from src.database import AsyncSession
from src.services.auth import AuthService
from src.api.dependencies import DBDep, AuthUserDep
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.post("/login")
async def login_user(
        data: UserLoginSchema,
        response: Response
):
    async with AsyncSession() as session:
        user = await UsersRepository(session).get_user_with_hashed_pswd(username=data.username)
        if not user:
            raise HTTPException(status_code=401, detail="User with this username does not exist")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Password error!")
    access_token = AuthService().create_access_token({'user_id': user.id})
    response.set_cookie('access_token', access_token, secure=False)
    return {'access_token': access_token}


@router.post("/", summary="Добавление нового пользователя")
async def add_user(
        db: DBDep,
        data: UsersRequestSchema
):
    hashed_password = AuthService().hash_pswd(data.password)
    new_data = UserAddSchema(username=data.username, nik_name=data.nik_name, hashed_password=hashed_password)
    try:
        new_user = await db.usersModel.add_obj(new_data)
        await db.save()
    except IntegrityError:
        raise HTTPException(status_code=404, detail="Такой пользователь существует")
    return new_user


@router.get("/")
async def get_users():
    async with AsyncSession() as session:
        users = await UsersRepository(session).get_objects()
    return users


@router.get("/get_user")
async def get_users(user_id: AuthUserDep):
    return user_id


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie('access_token')
    return {'success': "Вы вышли из аккаунта"}


