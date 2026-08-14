from product.db.session import SessionLocal
from product.models.user import User
from product.utils.security import hash_password


TEST_USERS = [
    {
        "name": "prachi",
        "email": "p@mail.com",
        "password": "prachi123",
        "mobile": "9010420106",
        "role": "admin",
    },
    {
        "name": "murali",
        "email": "m@mail.com",
        "password": "murali123",
        "mobile": "9999999998",
        "role": "support",
    },
]


def seed_users() -> None:
    db = SessionLocal()

    try:
        for user_data in TEST_USERS:
            email = user_data["email"].strip().lower()

            existing_user = (
                db.query(User)
                .filter(User.Email == email)
                .first()
            )

            if existing_user is not None:
                existing_user.Name = user_data["name"]
                existing_user.Mobile = user_data["mobile"]
                existing_user.Role = user_data["role"]
                existing_user.Password = hash_password(
                    user_data["password"]
                )
                continue

            db.add(
                User(
                    Name=user_data["name"],
                    Email=email,
                    Password=hash_password(user_data["password"]),
                    Mobile=user_data["mobile"],
                    Role=user_data["role"],
                )
            )

        db.commit()
        print("Admin and support users created or updated successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_users()
