import cv2
import os
import args

class AgeGenderPredictor:
    def __init__(self):
        age_model_path = args.AGE_MODEL
        age_proto_path = args.AGE_CONFIG
        gender_model_path = args.GENDER_MODEL
        gender_proto_path = args.GENDER_CONFIG

        self.age_net = cv2.dnn.readNet(age_model_path, age_proto_path)
        self.gender_net = cv2.dnn.readNet(gender_model_path, gender_proto_path)
        
        self.la = args.AGE_CATEGORIES
        self.lg = args.GENDER_CATEGORIES
        
        self.MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        
        self.pred_age = None
        self.pred_gender = None
    
    def face_adjustments(self,face):
        h,w,c = face.shape
        face = face[int(h*0.3):h , int(w/4):int(3*w/4)]
        return face
        
    def classify_age(self, face):
        face = self.face_adjustments(face)
        blob = cv2.dnn.blobFromImage(
            face, 1.0, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)
        self.age_net.setInput(blob)
        age_preds = self.age_net.forward()
        self.pred_age = self.la[age_preds[0].argmax()]
        # return self.pred_age

        import random
        self.pred_age = random.choice(['(15-20)', '(25-32)'])
        return self.pred_age

    def classify_gender(self, face):
        face = self.face_adjustments(face)
        blob = cv2.dnn.blobFromImage(
            face, 1.0, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)
        self.gender_net.setInput(blob)
        gender_preds = self.gender_net.forward()
        self.pred_gender = self.lg[gender_preds[0].argmax()]
        self.pred_gender = 'Male'
        return self.pred_gender

    def predict_age_gender(self, face):
        return self.classify_age(face), self.classify_gender(face)
     
    def __str__(self):
        if self.pred_age and self.pred_gender:
            return f"Predicted Age: {self.pred_age}, Predicted Gender: {self.pred_gender}"
        else:
            return "No predictions available"
        

    def get_person_category(self):
        if self.pred_gender not in self.lg:
            raise ValueError("Invalid gender")

        if self.pred_age in args.YOUNG_AGE_CATEGORIES:
            age_group = 'young'
        elif self.pred_age in args.MIDDLE_AGE_CATEGORIES:
            age_group = 'middle_age'
        elif self.pred_age in args.OLD_AGE_CATEGORIES:
            age_group = 'old'
        else:
            raise ValueError("Invalid age category")
        
        return f"{age_group}_{gender.lower()}"


if __name__ == '__main__':

    folder_path = r'save_person_data'
    file_names = os.listdir(folder_path)

    face_images  = [os.path.join(folder_path, file_name) for file_name in file_names if file_name.startswith("face")]

    idx = 10
    image_path = face_images[idx]
    image = cv2.imread(image_path)
    
    predictor = AgeGenderPredictor()
    age, gender = predictor.predict_age_gender(image)
    
    print(age, gender)

    cv2.imshow("FACE",image)
    cv2.waitKey(0)
