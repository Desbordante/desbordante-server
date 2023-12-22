from datetime import datetime
from app.db.models.user.user import AccountStatusType

user_data = [
    {
        # All fields are described
        "id": "473e6893-6407-4eba-a1e0-0328fa32a589",
        "email": "petr2003@gmail.com",
        "full_name": "Petr Petrovich",
        "country": "Russia",
        "company_or_affiliation": "company",
        "occupation": "occupation",
        "account_status": AccountStatusType.EMAIL_VERIFICATION,
        "hashed_password": "kdk3kdo3di2ofdni2o",
        "created_at": datetime.now(),
        "deleted_at": datetime.now(),
    },
    {
        # Without delete time
        "id": "2d9494ab-211b-4e8a-8f5e-5728ab4d5c9b",
        "email": "andrey2003@gmail.com",
        "full_name": "Andrey Petrovich",
        "country": "Russia",
        "company_or_affiliation": "company",
        "occupation": "occupation",
        "account_status": AccountStatusType.EMAIl_VERIFIED,
        "hashed_password": "dkd3kdk3ek33dd",
        "created_at": datetime.now(),
    },
    {
        # Without ID
        "id": "c6f0c516-6730-44ee-86b3-f7e487821cfe",
        "email": "kirillKirillovich@mail.ru",
        "full_name": "Kirill Kirillovich",
        "country": "Russia",
        "company_or_affiliation": "company",
        "occupation": "occupation",
        "account_status": AccountStatusType.EMAIl_VERIFIED,
        "hashed_password": "kdk3kdoddkdkdk3di2ofdni2o",
        "created_at": datetime.now(),
        "deleted_at": datetime.now(),
    },
    {
        # Without ID and delete time
        "email": "DmitryDmitrievich@mail.ru",
        "full_name": "Dmitry Dmitrievich",
        "country": "Russia",
        "company_or_affiliation": "company",
        "occupation": "occupation",
        "account_status": AccountStatusType.EMAIl_VERIFIED,
        "hashed_password": "krrr3r3dk3kdoddkdkdk3di2ofdni2o",
        "created_at": datetime.now(),
    },
    {
        # All fields are described
        "id": "8cb69c83-a2c6-4bce-a20c-a615d1d3f8dd",
        "email": "petyaaaGang1999@yandex.ru",
        "full_name": "Petr Ivanych",
        "country": "Russia",
        "company_or_affiliation": "company",
        "occupation": "occupation",
        "account_status": AccountStatusType.EMAIL_VERIFICATION,
        "hashed_password": "kdk3kdo3di2ofdni2o",
        "created_at": datetime.now(),
        "deleted_at": datetime.now(),
    },
    {
        # All fields are described
        "id": "5e5c3c27-c39f-4fe5-a1f2-be23271e62f1",
        "email": "kukreku2003@gmail.com",
        "full_name": "Ivan Ivanych",
        "country": "Russia",
        "company_or_affiliation": "company",
        "occupation": "occupation",
        "account_status": AccountStatusType.EMAIL_VERIFICATION,
        "hashed_password": "kfffssdk3kdo3di2ofdni2o",
        "created_at": datetime.now(),
        "deleted_at": datetime.now(),
    },
    {
        # All fields are described
        "id": "6d6d3c27-c39f-4fe5-a1f2-be23271e62f1",
        "email": "abcccccc@gmail.com",
        "full_name": "Lize Petrovna",
        "country": "Russia",
        "company_or_affiliation": "company",
        "occupation": "occupation",
        "account_status": AccountStatusType.EMAIL_VERIFICATION,
        "hashed_password": "ijieeic3oh484nch8h2£*edn3dnj3dxjx",
        "created_at": datetime.now(),
        "deleted_at": datetime.now(),
    },
]
