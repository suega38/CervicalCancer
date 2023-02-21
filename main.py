import kivy
from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.toast import toast
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
import pickle
import numpy as np
import mysql.connector
import re
from string import punctuation
from kivy.storage.jsonstore import JsonStore

class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    phone = ObjectProperty(None)
    
    def submit(self):
        #Define db
        mydb = mysql.connector.connect(
            host = "eu-cdbr-west-03.cleardb.net",
            user = "b6f89c172e4a67",
            passwd = "a957064b",
            db = "heroku_b20a166a83dfce0"
        )
        #cursor db
        c = mydb.cursor()

        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":

                command = "INSERT INTO user (`name`, `email`, `password`, `phone`) VALUES (%s, %s, %s,%s);"
                values = (self.namee.text, self.email.text, self.password.text, self.phone.text)
                
                #execute sql command
                c.execute (command,values)

                mydb.commit()

                mydb.close()

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def homeBtn(self):
        self.reset()
        sm.current = "welcome"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""
        self.phone.text = ""


class LoginWindow(Screen):
    namee = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        
        #get name n password from screen
        app = App.get_running_app()
        name = self.namee.text 
        password = self.password.text   
        
        #Define db
        mydb = mysql.connector.connect(
            host = "eu-cdbr-west-03.cleardb.net",
            user = "b6f89c172e4a67",
            passwd = "a957064b",
            db = "heroku_b20a166a83dfce0"
        )
        #cursor db
        c = mydb.cursor()

        #grab data
        c.execute("SELECT name, password FROM user where name = '"+str(name)+"' and password = '"+str(password)+"'")

        records = c.fetchone()
        print (records)

        count = records

        #verify
        if count == None :
            pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(300, 110))
            pop.open()    
        else:
            sm.current = "home"

        c.execute("SELECT user_id FROM user where name = '"+str(name)+"' and password = '"+str(password)+"'")
        id = c.fetchone()

        userid = str(id)
        user = re.sub(f"[{re.escape(punctuation)}]", "", userid)
        print (user)
        
        global n
        n = user

        mydb.commit()

        mydb.close

    def homeBtn(self):
        sm.current = "welcome"

    def reset(self):
        self.namee.text = ""
        self.password.text = ""


class WelcomeWindow(Screen):
   
    def logIn(self):
        sm.current = "login"

    def create(self):
        sm.current = "create"

class HomeWindow(Screen):
   
    def record(self):
        sm.current = "record"

    def predict(self):
        sm.current = "predict"

class RecordWindow(Screen):
    output = ObjectProperty(None)
    age = ObjectProperty(None)
    smoke = ObjectProperty(None)
    smokeDuration = ObjectProperty(None)
    famHistory = ObjectProperty(None)
    std = ObjectProperty(None)
    hiv = ObjectProperty(None)
    pregnancy = ObjectProperty(None)
    contraception = ObjectProperty(None)
    sexualPartners = ObjectProperty(None)
    pastResult = ObjectProperty(None)
    current = ""

    def on_enter(self, *args):
        global n
        print(n)
         
        #Define db
        mydb = mysql.connector.connect(
            host = "eu-cdbr-west-03.cleardb.net",
            user = "b6f89c172e4a67",
            passwd = "a957064b",
            db = "heroku_b20a166a83dfce0"
        )
        #cursor db
        c = mydb.cursor()


        c.execute("SELECT result FROM user where user_id = '"+str(n)+"'")
        output = c.fetchone()
        output = str(output)

        c.execute("SELECT age FROM user where user_id = '"+str(n)+"'")
        age = c.fetchone()
        age = str(age)
 
        c.execute("SELECT smoke FROM user where user_id = '"+str(n)+"'")
        smoke = c.fetchone()
        smoke = str(smoke)

        c.execute("SELECT smokeD FROM user where user_id = '"+str(n)+"'")
        smokeDuration = c.fetchone()
        smokeDuration = str(smokeDuration)

        c.execute("SELECT famH FROM user where user_id = '"+str(n)+"'")
        famHistory = c.fetchone()
        famHistory = str(famHistory)

        c.execute("SELECT std FROM user where user_id = '"+str(n)+"'")
        std = c.fetchone()
        std = str(std)

        c.execute("SELECT hiv FROM user where user_id = '"+str(n)+"'")
        hiv = c.fetchone()
        hiv = str(hiv)

        c.execute("SELECT pregnancy FROM user where user_id = '"+str(n)+"'")
        pregnancy = c.fetchone()
        pregnancy = str(pregnancy)

        c.execute("SELECT contraception FROM user where user_id = '"+str(n)+"'")
        contraception = c.fetchone()
        contraception = str(contraception)

        c.execute("SELECT sexualP FROM user where user_id = '"+str(n)+"'")
        sexualPartners = c.fetchone()
        sexualPartners = str(sexualPartners)

        output = re.sub(f"[{re.escape(punctuation)}]", "", output)
        age = re.sub(f"[{re.escape(punctuation)}]", "", age)
        smoke = re.sub(f"[{re.escape(punctuation)}]", "", smoke)
        smokeDuration = re.sub(f"[{re.escape(punctuation)}]", "", smokeDuration)
        famHistory = re.sub(f"[{re.escape(punctuation)}]", "", famHistory)
        std = re.sub(f"[{re.escape(punctuation)}]", "", std)
        hiv = re.sub(f"[{re.escape(punctuation)}]", "", hiv)
        pregnancy = re.sub(f"[{re.escape(punctuation)}]", "", pregnancy)
        contraception = re.sub(f"[{re.escape(punctuation)}]", "", contraception)
        sexualPartners = re.sub(f"[{re.escape(punctuation)}]", "", sexualPartners)
        
        mydb.commit()

        mydb.close()
        self.output.text = output + " risk"
        self.age.text = "Age: " + age
        self.smoke.text = "Smoke (1=no, 2=yes): " + smoke
        self.smokeDuration.text= "Smoke Duration (years): " + smokeDuration
        self.famHistory.text = "Family History of Cervical Cancer (1=no, 2=yes): " + famHistory
        self.std.text = "STD (1=no, 2=yes): " + std
        self.hiv.text = "HIV (1=no, 2=yes): " + hiv
        self.pregnancy.text= "Numbers of pregnancy: " + pregnancy
        self.contraception.text = "Contraception (1=no, 2=yes): " + contraception
        self.sexualPartners.text= "Number of sexual partners: " + sexualPartners


class PredictWindow(Screen, Widget):
    age = ObjectProperty(None)
    smokeDuration = ObjectProperty(None)
    pregnancy = ObjectProperty(None)
    sexualPartners = ObjectProperty(None)

    def checkbox_smoke(self, instance, value, smoke):
        print(smoke)
        if value == True:
            sm = f'{smoke}'
            mydb = mysql.connector.connect(
            host = "eu-cdbr-west-03.cleardb.net",
            user = "b6f89c172e4a67",
            passwd = "a957064b",
            db = "heroku_b20a166a83dfce0"
            )
            #cursor db
            c = mydb.cursor()
            c.execute("UPDATE user SET smoke = '"+str(sm)+"' WHERE user_id = '"+str(n)+"';")
            mydb.commit()

            mydb.close()

    def checkbox_fam(self, instance, value, famHistory):
        print(famHistory)
        if value == True:
            sm = f'{famHistory}'
            mydb = mysql.connector.connect(
            host = "eu-cdbr-west-03.cleardb.net",
            user = "b6f89c172e4a67",
            passwd = "a957064b",
            db = "heroku_b20a166a83dfce0"
            )
            #cursor db
            c = mydb.cursor()
            c.execute("UPDATE user SET famH = '"+str(sm)+"' WHERE user_id = '"+str(n)+"';")
            mydb.commit()

            mydb.close()

    def checkbox_hiv(self, instance, value, hiv):
        print(hiv)
        if value == True:
            sm = f'{hiv}'
            mydb = mysql.connector.connect(
            host = "eu-cdbr-west-03.cleardb.net",
            user = "b6f89c172e4a67",
            passwd = "a957064b",
            db = "heroku_b20a166a83dfce0"
            )
            #cursor db
            c = mydb.cursor()
            c.execute("UPDATE user SET hiv = '"+str(sm)+"' WHERE user_id = '"+str(n)+"';")
            mydb.commit()

            mydb.close()

    def checkbox_std(self, instance, value, std):
        print(std)
        if value == True:
            sm = f'{std}'
            mydb = mysql.connector.connect(
            host = "eu-cdbr-west-03.cleardb.net",
            user = "b6f89c172e4a67",
            passwd = "a957064b",
            db = "heroku_b20a166a83dfce0"
            )
            #cursor db
            c = mydb.cursor()
            c.execute("UPDATE user SET std = '"+str(sm)+"' WHERE user_id = '"+str(n)+"';")
            mydb.commit()

            mydb.close()

    def checkbox_click(self, instance, value, contraception):
        if value == True:
            sm = f'{contraception}'
            mydb = mysql.connector.connect(
            host = "eu-cdbr-west-03.cleardb.net",
            user = "b6f89c172e4a67",
            passwd = "a957064b",
            db = "heroku_b20a166a83dfce0"
            )
            #cursor db
            c = mydb.cursor()
            c.execute("UPDATE user SET contraception = '"+str(sm)+"' WHERE user_id = '"+str(n)+"';")
            mydb.commit()

            mydb.close()

    def submitP(self):
        global n
        print(n)  

         #Define db
        mydb = mysql.connector.connect(
            host = "eu-cdbr-west-03.cleardb.net",
            user = "b6f89c172e4a67",
            passwd = "a957064b",
            db = "heroku_b20a166a83dfce0"
        )
        #cursor db
        c = mydb.cursor()

        c.execute("UPDATE user SET age = '"+str(self.age.text)+"' WHERE user_id = '"+str(n)+"';")
        c.execute("UPDATE user SET smokeD = '"+str(self.smokeDuration.text)+"' WHERE user_id = '"+str(n)+"';")
        c.execute("UPDATE user SET pregnancy = '"+str(self.pregnancy.text)+"' WHERE user_id = '"+str(n)+"';")
        c.execute("UPDATE user SET sexualP = '"+str(self.sexualPartners.text)+"' WHERE user_id = '"+str(n)+"';")

        mydb.commit()

        mydb.close()

        sm.current = "result"

class ResultWindow(Screen):
    output = ObjectProperty(None)
    
    def on_enter(self, *args):

        global n
        print(n)

        loaded_model=pickle.load(open("cancermodel.pkl",'rb'))

         #Define db
        mydb = mysql.connector.connect(
            host = "eu-cdbr-west-03.cleardb.net",
            user = "b6f89c172e4a67",
            passwd = "a957064b",
            db = "heroku_b20a166a83dfce0"
        )
        #cursor db
        c = mydb.cursor()

        c.execute("SELECT age FROM user where user_id = '"+str(n)+"'")
        age = c.fetchone()
        age = str(age)
        age = re.sub(f"[{re.escape(punctuation)}]", "", age)
        age = int(age)
        print(age)

        c.execute("SELECT smoke FROM user where user_id = '"+str(n)+"'")
        smoke = c.fetchone()
        smoke = str(smoke)
        print(smoke)
        smoke = re.sub(f"[{re.escape(punctuation)}]", "", smoke)
        smoke = int(smoke)
        print(smoke)

        c.execute("SELECT smokeD FROM user where user_id = '"+str(n)+"'")
        smokeD = c.fetchone()
        smokeD = str(smokeD)
        smokeD = re.sub(f"[{re.escape(punctuation)}]", "", smokeD)
        smokeD = int(smokeD)

        c.execute("SELECT famH FROM user where user_id = '"+str(n)+"'")
        famH = c.fetchone()
        famH = str(famH)
        famH = re.sub(f"[{re.escape(punctuation)}]", "", famH)
        famH = int(famH)


        c.execute("SELECT std FROM user where user_id = '"+str(n)+"'")
        std = c.fetchone()
        std = str(std)
        std = re.sub(f"[{re.escape(punctuation)}]", "", std)
        std = int(std)

        c.execute("SELECT hiv FROM user where user_id = '"+str(n)+"'")
        hiv = c.fetchone()
        hiv = str(hiv)
        hiv = re.sub(f"[{re.escape(punctuation)}]", "", hiv)
        hiv = int(hiv)

        c.execute("SELECT pregnancy FROM user where user_id = '"+str(n)+"'")
        pregnancy = c.fetchone()
        pregnancy = str(pregnancy)
        pregnancy = re.sub(f"[{re.escape(punctuation)}]", "", pregnancy)
        pregnancy = int(pregnancy)

        c.execute("SELECT contraception FROM user where user_id = '"+str(n)+"'")
        contraception = c.fetchone()
        contraception = str(contraception)
        contraception = re.sub(f"[{re.escape(punctuation)}]", "", contraception)
        contraception = int(contraception)

        c.execute("SELECT sexualP FROM user where user_id = '"+str(n)+"'")
        sexualP = c.fetchone()
        sexualP = str(sexualP)
        sexualP = re.sub(f"[{re.escape(punctuation)}]", "", sexualP)
        sexualP = int(sexualP)

        input_data=(age,smoke ,smokeD ,famH ,std ,hiv, pregnancy,contraception ,sexualP)

        # change input_data to numpy array
        inp_data_as_numpy_arr= np.asarray(input_data)
        print(f"1D Data : {inp_data_as_numpy_arr}\n")

        # input data reshape because model is expecting 2D array or all data , we'll reshape our 1d data to 2d and feed our model an instance
        inp_data_reshape=inp_data_as_numpy_arr.reshape(1,-1)
        print(f"2D Data : {inp_data_reshape}\n")


        # prediction
        prediction = loaded_model.predict(inp_data_reshape)
        print(f"Predicted Value: {prediction}")
        if(prediction[0]== 1):
            result = "normal"
            print("This person has less risk of cervical cancer")
        else:
            print("This person is at risk of cervical cancer")
            result = "high"

        c.execute("UPDATE user SET result = '"+str(result)+"' WHERE user_id = '"+str(n)+"';")

        self.output.text = result + " risk"

        mydb.commit()

        mydb.close()

class ProfileWindow(Screen):
    name = ObjectProperty(None)
    email = ObjectProperty(None)
    phone = ObjectProperty(None)
    password = ObjectProperty(None)
    current = ""
    
    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):

        global n
        print(n)
         
        #Define db
        mydb = mysql.connector.connect(
            host = "eu-cdbr-west-03.cleardb.net",
            user = "b6f89c172e4a67",
            passwd = "a957064b",
            db = "heroku_b20a166a83dfce0"
        )
        #cursor db
        c = mydb.cursor()


        c.execute("SELECT name FROM user where user_id = '"+str(n)+"'")
        name = c.fetchone()
        name = str(name)

        c.execute("SELECT email FROM user where user_id = '"+str(n)+"'")
        email = c.fetchone()
        email = str(email)

        c.execute("SELECT phone FROM user where user_id = '"+str(n)+"'")
        phone = c.fetchone()
        phone = str(phone)

        c.execute("SELECT password FROM user where user_id = '"+str(n)+"'")
        password = c.fetchone()
        password = str(password)

        name = re.sub(f"[{re.escape(punctuation)}]", "", name)
        email = re.sub(f"[{re.escape(',')}]", "", email)
        phone = re.sub(f"[{re.escape(punctuation)}]", "", phone)
        password = re.sub(f"[{re.escape(punctuation)}]", "", password)

        self.namee.text = "Name: " + name
        self.email.text = "Email Address: " + email
        self.phone.text = "Contact Number: " + phone
        self.password.text= "Password: " + password
        
        mydb.commit()

        mydb.close()


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(300, 110))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 110))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),ProfileWindow(name="profile"),WelcomeWindow(name="welcome"), 
HomeWindow(name="home"), RecordWindow(name="record"), PredictWindow(name="predict"), ResultWindow(name="result")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "welcome"

class MyMainApp(App):
    def build(self):
        Window.clearcolor = (1,1,1,1)
        #Define db
        mydb = mysql.connector.connect(
            host = "eu-cdbr-west-03.cleardb.net",
            user = "b6f89c172e4a67",
            passwd = "a957064b",
            db = "heroku_b20a166a83dfce0"
        )
        #cursor db
        c = mydb.cursor()

        #check database
        c.execute("SHOW DATABASES")
        for db in c:
            print(db)
            

        return sm


if __name__ == "__main__":
    MyMainApp().run()