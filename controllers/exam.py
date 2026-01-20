from sqlalchemy.orm import Session
import time
from ..models import Module, Professeur, LieuExamen, Examen
import random
from datetime import datetime, timedelta

def generate_smart_exam_schedule(db: Session, start_date: datetime):
    start_time = time.time()  # record start

    all_modules = db.query(Module).all()
    all_professors = db.query(Professeur).all()
    all_rooms = db.query(LieuExamen).all()

    if not all_modules or not all_professors or not all_rooms:
        return {"error": "Missing data (modules, profs, or rooms)"}

    db.query(Examen).delete()
    
    exams_to_create = []
    
    time_slots = [9, 11, 14] 
    current_day =   datetime.strptime(start_date, "%Y-%m-%d")

    occupied_profs = set()
    occupied_rooms = set()
    
    random.shuffle(all_modules)

    for module in all_modules:
        assigned = False
        attempts = 0
        
        while not assigned and attempts < 100:  

            day_offset = random.randint(0, 14)  
            slot = random.choice(time_slots)
            exam_time = current_day.replace(hour=slot, minute=0, second=0) + timedelta(days=day_offset)
            
            day_str = exam_time.strftime("%Y-%m-%d")
            
            prof = random.choice(all_professors)
            room = random.choice(all_rooms)
            
            prof_key = (day_str, slot, prof.id)
            room_key = (day_str, slot, room.id)
            
            if prof_key not in occupied_profs and room_key not in occupied_rooms:
                new_exam = Examen(
                    module_id=module.id,
                    prof_id=prof.id,
                    salle_id=room.id,
                    date_heure=exam_time,
                    duree_minutes=90   
                )
                exams_to_create.append(new_exam)
                
                occupied_profs.add(prof_key)
                occupied_rooms.add(room_key)
                assigned = True
            
            attempts += 1

    try:
        db.bulk_save_objects(exams_to_create)
        db.commit()
        end_time = time.time()  # record end
        execution_time = end_time - start_time  # in seconds

        print(f"Function execution time: {execution_time:.6f} seconds")
        return {"status": "Success", "exams_count": len(exams_to_create)}
    except Exception as e:
        db.rollback()
        return {"status": "Error", "message": str(e)}