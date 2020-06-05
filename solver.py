from constants import *
from db import *
from objects import POSTFIX, PREFIX, KEYBOARDS
from paginator import Paginator

import json


class Solver:
    def __validate(self, req_params, params):
        try:
            for param_name in req_params:
                if not params[param_name]:
                    return False
                    # if hasattr(contex, param_name):
                        # params[param_name] = getattr(contex, param_name).name
                    # else:
                        # return False
            return True
        except:
            return False
    
    def __add_new_user(self, id):
        try:
            user = User.create(id = id)
            return user
        except:
            return False

    def __get_user_contex(self, id):
        try:
            #if this is old user, we just get his instance
            user = User.get(User.id == id)
        except:
            #if this is new user, we create new user instace
            user = self.__add_new_user(id)
        try:
            contex = Contex.get(Contex.user == user)
        except:
            contex = Contex.create(user = user, )
        return contex
    
    def __update_contex(self, contex, fields):
        for key, value in fields.items():
            setattr(contex, key, value)
        contex.save()
    
    def __clear_contex(self, contex, mode):
        if mode == "SUB":
            contex.paginator_page = 1
            contex.save()
            ContexSubject.delete().where(ContexSubject.contex == contex).execute()
            return True
        elif mode == "SPH":
            contex.paginator_page = 1
            contex.save()
            ContexSphere.delete().where(ContexSphere.contex == contex).execute()
            return True
        elif mode == "ALL":
            contex.paginator_page = 1
            contex.save()
            ContexSubject.delete().where(ContexSubject.contex == contex).execute()
            ContexSphere.delete().where(ContexSphere.contex == contex).execute()
            return True
        else:
            return True
        

    def run(self, intent, params, peer_id):
        # contex = self.__get_user_contex(peer_id)
        DEFAULT_PARAMS = {"keyboard": json.dumps(KEYBOARDS["default"])}
        
        if intent == DIRECTION_GET:
            REQUIRED_PARAMS = ["direction"]
            if not self.__validate(REQUIRED_PARAMS, params):
                return False, DEFAULT_PARAMS
            result = Direction.get(Direction.name==params["direction"].lower().strip())
            # self.__update_contex(contex, {"direction": result})
            response = f'Лови ссылку на направление {result.name}: {result.url}' 
            return response, DEFAULT_PARAMS
        
        elif intent == DIRECTION_GET_POINTS:
            REQUIRED_PARAMS = ["direction"]
            if not self.__validate(REQUIRED_PARAMS, params):
                return False, DEFAULT_PARAMS
            result = Direction.get(Direction.name==params["direction"].lower().strip())
            # self.__update_contex(contex, {"direction": result})
            response = f'Минимальные баллы на направление "{result.name}":\nКонтракт: {result.ball_k}\nБюджет: {result.ball_b}' 
            return response, DEFAULT_PARAMS
        
        elif intent == DIRECTION_GET_BY_SUBJECTS:
            contex = self.__get_user_contex(peer_id)
            self.__clear_contex(contex, mode = "SUB")
            REQUIRED_PARAMS = ["subjects"]
            if not self.__validate(REQUIRED_PARAMS, params):
                return False, DEFAULT_PARAMS
            directions = Direction.select(Direction.name).execute()
            directions = set([t.name for t in directions])
            for subject in params["subjects"]:
                subquery = Subject.get(Subject.name==subject)
                ContexSubject.insert({"contex": contex, "subject": subquery}).execute()
                temp = (DirectionSubject
                       .select(DirectionSubject.direction)
                       .where(DirectionSubject.subject==subquery).execute())
                temp = set([t.direction.name for t in temp if t.direction.active]) #convert to set
                directions = directions & temp
            response = ""
            paginator = Paginator(contex, contex.paginator_page, 3, list(directions))
            directions, is_last = paginator.next()
            response = ""
            if directions:
                for direction in directions:
                    temp = Direction.get(Direction.name == direction)
                    response += f"Факультет: {temp.faculty}\nНаправление: {direction}\nСсылка: {temp.url}\n\n" 
                if not is_last:
                    params = {"keyboard": json.dumps(KEYBOARDS["direction_by_subjects"])}
                else:
                    params = {"keyboard": json.dumps(KEYBOARDS["default"])}
            else:
                response = "Я ничего не нашел.\nПопробуй поменять предметы."
            return response, params
        
        elif intent == DIRECTION_GET_BY_SPHERES:
            contex = self.__get_user_contex(peer_id)
            self.__clear_contex(contex, mode = "SPH")
            REQUIRED_PARAMS = ["spheres"]
            if not self.__validate(REQUIRED_PARAMS, params):
                return False, DEFAULT_PARAMS
            directions = Direction.select(Direction.name).execute()
            directions = set([t.name for t in directions])
            for sphere in params["spheres"]:
                subquery = Sphere.get(Sphere.name==sphere)
                ContexSphere.insert({"contex": contex, "sphere": subquery}).execute()
                temp = (DirectionSphere
                       .select(DirectionSphere.direction)
                       .where(DirectionSphere.sphere==subquery).execute())
                temp = set([t.direction.name for t in temp if t.direction.active]) #convert to set
                directions = directions & temp
            response = ""
            paginator = Paginator(contex, contex.paginator_page, 3, list(directions))
            directions, is_last = paginator.next()
            response = ""
            if directions:
                for direction in directions:
                    temp = Direction.get(Direction.name == direction)
                    response += f"Факультет: {temp.faculty}\nНаправление: {direction}\nСсылка: {temp.url}\n\n" 
                if not is_last:
                    params = {"keyboard": json.dumps(KEYBOARDS["direction_by_spheres"])}
                else:
                    params = {"keyboard": json.dumps(KEYBOARDS["default"])}
            return response, params
        
        elif intent == DIRECTION_GET_SUBJECTS:
            REQUIRED_PARAMS = ["direction"]
            if not self.__validate(REQUIRED_PARAMS, params):
                return False, DEFAULT_PARAMS
            direction = Direction.get(Direction.name==params["direction"].lower())
            query = (DirectionSubject
                        .select()
                        .where(DirectionSubject.direction == direction)
                        .execute())
            subjects = [ t.subject.name for t in query ]
            response = ""
            i = 1
            response = f"Для поступления на направление {direction.name} необходимы следующие предметы:"
            for subject in subjects:
                response += f"\n{i}.{subject}" 
                i+=1
            if not direction.active:
                response += f"\n\n Обрати внимание, что на данный момент это направление не активно и прием документов на него не ведется."
            return response, DEFAULT_PARAMS
        
        
        elif intent == FACULTY_GET:
            REQUIRED_PARAMS = ["faculty"]
            if not self.__validate(REQUIRED_PARAMS, params):
                return False, DEFAULT_PARAMS
            result = Faculty.get(Faculty.name == params["faculty"].upper().strip())
            # self.__update_contex(contex, {"faculty": result})
            response = f'Лови ссылку на факультет {params["faculty"].upper()}: {result.url}'
            return response, DEFAULT_PARAMS
        else:
            return False, False
    
    def resolve_payload(self, payload, id):
        DEFAULT_PARAMS = {"keyboard": json.dumps(KEYBOARDS["default"])}
        contex = self.__get_user_contex(id)
        payload = json.loads(payload)        
        if payload["command"] == "direction.by_subjects.more":
            subjects = (ContexSubject.select(ContexSubject.subject)
                        .where(ContexSubject.contex == contex).execute())
            subjects = [s.subject.name for s in subjects]
            directions = Direction.select(Direction.name).execute()
            directions = set([t.name for t in directions])
            for subject in subjects:
                subquery = Subject.get(Subject.name==subject)
                temp = (DirectionSubject
                       .select(DirectionSubject.direction)
                       .where(DirectionSubject.subject==subquery).execute())
                temp = set([t.direction.name for t in temp if t.direction.active]) #convert to set
                directions = directions & temp    
            paginator = Paginator(contex, contex.paginator_page, 3, list(directions))
            directions, is_last = paginator.next()
            response = ""
            if directions:
                for direction in directions:
                    temp = Direction.get(Direction.name == direction)
                    response += f"Факультет: {temp.faculty}\nНаправление: {direction}\nСсылка: {temp.url}\n\n" 
                if not is_last:
                    params = {"keyboard": json.dumps(KEYBOARDS["direction_by_subjects"])}
                else:
                    params = {"keyboard": json.dumps(KEYBOARDS["default"])}
                    response += "Это все, что я нашел."
            return response, params

        elif payload["command"] == "direction.by_spheres.more":
            spheres = (ContexSphere.select(ContexSphere.sphere)
                        .where(ContexSphere.contex == contex).execute())
            spheres = [s.sphere.name for s in spheres]
            directions = Direction.select(Direction.name).execute()
            directions = set([t.name for t in directions])
            for sphere in spheres:
                subquery = Sphere.get(Sphere.name==sphere)
                temp = (DirectionSphere
                       .select(DirectionSphere.direction)
                       .where(DirectionSphere.sphere==subquery).execute())
                temp = set([t.direction.name for t in temp if t.direction.active]) #convert to set
                directions = directions & temp    
            paginator = Paginator(contex, contex.paginator_page, 3, list(directions))
            directions, is_last = paginator.next()
            response = ""
            if directions:
                for direction in directions:
                    temp = Direction.get(Direction.name == direction)
                    response += f"Факультет: {temp.faculty}\nНаправление: {direction}\nСсылка: {temp.url}\n\n" 
                if not is_last:
                    params = {"keyboard": json.dumps(KEYBOARDS["direction_by_spheres"])}
                else:
                    params = {"keyboard": json.dumps(KEYBOARDS["default"])}
                    response += "Это все, что я нашел."
                return response, params

        elif payload["command"] == "direction.cancel":
            self.__clear_contex(contex, "ALL") 
            return "Готово", DEFAULT_PARAMS




    def set_prefix(self, intent, params):
        return ""
    
    def set_postfix(self, intent, params):
        try:
            if intent == FACULTY_GET and not params['faculty']:
                return POSTFIX[FACULTY_GET]['faculty']
            
            elif intent == DIRECTION_GET_POINTS and params['faculty']:
                faculty = Faculty.get(Faculty.name == params['faculty'])
                directions = (Direction.select()
                              .where(Direction.faculty == faculty.name)
                              .execute())
                directions = [d.name for d in directions if d.active]
                response = f"\n\nНа факультете {faculty.name} доступны следующие направления:\n"
                i = 1
                for direction in directions:
                    response += f"\n{i}.{direction}"
                    i+=1
                response += "\n\nВведите название направления:"
                return response
            else:
                return ""
        except:
            return ""
            

        