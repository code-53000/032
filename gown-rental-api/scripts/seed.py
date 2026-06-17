import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, time, timedelta

from app.database import engine, SessionLocal, Base
from app.models import User, UserRole, Gown, GownStatus, GownStyle, Appointment, AppointmentStatus, RentalOrder, RentalStatus, GownCare, CareType, CareStatus
from app.utils.auth import get_password_hash


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if db.query(User).first():
            print("Seed data already exists, skipping.")
            return

        demo_bride = User(
            username="bride_demo",
            hashed_password=get_password_hash("123456"),
            name="张小美",
            phone="13800001111",
            role=UserRole.BRIDE,
        )
        demo_consultant = User(
            username="consultant_demo",
            hashed_password=get_password_hash("123456"),
            name="李顾问",
            phone="13800002222",
            role=UserRole.CONSULTANT,
        )
        db.add_all([demo_bride, demo_consultant])
        db.flush()

        gowns_data = [
            {"name": "月光童话", "designer": "Vera Wang", "style": GownStyle.BALL_GOWN, "color": "象牙白", "size": "M", "rental_price": 5800.0, "description": "经典蓬蓬裙摆，手工蕾丝绣花，梦幻公主风"},
            {"name": "星河漫步", "designer": "Pronovias", "style": GownStyle.MERMAID, "color": "香槟金", "size": "S", "rental_price": 4800.0, "description": "修身鱼尾设计，水钻点缀，优雅知性"},
            {"name": "晨曦微露", "designer": "Oscar de la Renta", "style": GownStyle.A_LINE, "color": "樱花粉", "size": "M", "rental_price": 3600.0, "description": "轻盈A字裙摆，薄纱渐变，浪漫清新"},
            {"name": "冰雪奇缘", "designer": "Zuhair Murad", "style": GownStyle.BALL_GOWN, "color": "珍珠白", "size": "L", "rental_price": 7200.0, "description": "重工水晶刺绣，大拖尾，华丽气场全开"},
            {"name": "仲夏夜之梦", "designer": "Elie Saab", "style": GownStyle.SHEATH, "color": "月光银", "size": "S", "rental_price": 5200.0, "description": "丝滑缎面，简约廓形，高级质感"},
            {"name": "花嫁物语", "designer": "Marchesa", "style": GownStyle.TRUMPET, "color": "薰衣草紫", "size": "M", "rental_price": 4500.0, "description": "立体花卉装饰，小拖尾，柔美仙气"},
            {"name": "云端漫步", "designer": "Carolina Herrera", "style": GownStyle.A_LINE, "color": "天际蓝", "size": "M", "rental_price": 3900.0, "description": "清新蓝色系，层叠薄纱，灵动飘逸"},
            {"name": "鎏金岁月", "designer": "Reem Acra", "style": GownStyle.MERMAID, "color": "古铜金", "size": "L", "rental_price": 6500.0, "description": "复古金色刺绣，紧致鱼尾，华贵典雅"},
            {"name": "清风明月", "designer": "Monique Lhuillier", "style": GownStyle.EMPIRE, "color": "薄荷绿", "size": "S", "rental_price": 3200.0, "description": "高腰帝国线，轻盈雪纺，田园诗意"},
            {"name": "红妆十里", "designer": "Guo Pei", "style": GownStyle.BALL_GOWN, "color": "中国红", "size": "M", "rental_price": 8800.0, "description": "中式嫁衣，金线盘绣，传统与时尚融合"},
        ]

        image_prompts = [
            "elegant+white+ball+gown+wedding+dress+lace",
            "champagne+mermaid+wedding+dress+crystal",
            "pink+a-line+wedding+dress+tulle",
            "white+ball+gown+wedding+dress+crystal+embroidery",
            "silver+sheath+wedding+dress+satin",
            "purple+trumpet+wedding+dress+floral",
            "blue+a-line+wedding+dress+tulle",
            "gold+mermaid+wedding+dress+vintage",
            "green+empire+wedding+dress+chiffon",
            "red+chinese+wedding+dress+embroidery",
        ]

        gowns = []
        for i, g in enumerate(gowns_data):
            gown = Gown(
                name=g["name"],
                designer=g["designer"],
                style=g["style"],
                color=g["color"],
                size=g["size"],
                image_url=f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={image_prompts[i]}&image_size=portrait_4_3",
                rental_price=g["rental_price"],
                description=g["description"],
            )
            gowns.append(gown)
        db.add_all(gowns)
        db.flush()

        today = date.today()
        appointments_data = [
            {"gown_idx": 0, "date": today + timedelta(days=3), "start": time(10, 0), "end": time(11, 0), "status": AppointmentStatus.CONFIRMED},
            {"gown_idx": 2, "date": today + timedelta(days=3), "start": time(14, 0), "end": time(15, 0), "status": AppointmentStatus.CONFIRMED},
            {"gown_idx": 4, "date": today + timedelta(days=5), "start": time(10, 0), "end": time(11, 30), "status": AppointmentStatus.PENDING},
            {"gown_idx": 1, "date": today + timedelta(days=7), "start": time(13, 0), "end": time(14, 0), "status": AppointmentStatus.PENDING},
            {"gown_idx": 5, "date": today + timedelta(days=10), "start": time(15, 0), "end": time(16, 30), "status": AppointmentStatus.PENDING},
        ]

        for a in appointments_data:
            apt = Appointment(
                gown_id=gowns[a["gown_idx"]].id,
                bride_id=demo_bride.id,
                consultant_id=demo_consultant.id,
                appointment_date=a["date"],
                start_time=a["start"],
                end_time=a["end"],
                status=a["status"],
            )
            db.add(apt)
        db.flush()

        rental = RentalOrder(
            gown_id=gowns[3].id,
            bride_id=demo_bride.id,
            consultant_id=demo_consultant.id,
            pickup_date=today + timedelta(days=1),
            return_date=today + timedelta(days=4),
            status=RentalStatus.ACTIVE,
            total_price=gowns[3].rental_price * 4,
        )
        db.add(rental)
        gowns[3].status = GownStatus.RENTED

        care = GownCare(
            gown_id=gowns[7].id,
            care_type=CareType.CLEANING,
            status=CareStatus.IN_PROGRESS,
            notes="干洗保养中",
            cost=300.0,
        )
        db.add(care)
        gowns[7].status = GownStatus.CLEANING

        db.commit()
        print("Seed data inserted successfully!")
        print(f"  Demo bride:      username=bride_demo      password=123456")
        print(f"  Demo consultant:  username=consultant_demo  password=123456")

    except Exception as e:
        db.rollback()
        print(f"Seed error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
