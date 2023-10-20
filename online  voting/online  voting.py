import smtplib
from email.mime.text import MIMEText

from flask import Flask,render_template,request,redirect,session
import datetime
from DBConnection import Db
import random
app = Flask(__name__)
app.secret_key="123"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['get','post'])
def login():
    if request.method=="POST":
        username=request.form['textfield']
        password=request.form['textfield2']
        db=Db()
        res=db.selectOne("select * from login where username='"+username+"' and password='"+password+"' ")
        if res is not None:
            session['head']=''
            if res['usertype']=='admin':
                session['lg']="lin"
                session['e']=username
                return redirect('/admin_home')
            elif res['usertype']=='student':
                session['e'] = username
                session['lid']=res['login_id']
                session['lg']="lin"

                return redirect('/student_home')

            elif res['usertype'] == 'candidate':
                session['lid'] = res['login_id']
                session['lg'] = "lin"
                return redirect('/candidate_home')
            else:
                return '<script>alert("incorrect");window.location="/"</script>'
        else:
            return '<script>alert("wrong password");window.location="/"</script>'
    return render_template('admin/login.html')

@app.route('/admin_home')
def admin_home():
    return render_template('admin/adminindex.html')
@app.route('/add_course',methods=['get','post'])
def add_course():
    session['head']="add course"
    if session['lg']=="lin":
        if request.method=="POST":
            course_name=request.form['textfield']
            department= request.form['select']
            db=Db()
            db.insert("insert into course VALUES ('','"+course_name+"','"+department+"')")
            return '<script>alert("successfully added");window.location="/add_course"</script>'
        else:
            db=Db()
            res= db.select("select * from department")
            return render_template('admin/add course.html',data=res)
    else:
        return redirect('/')

@app.route('/add_election',methods=['get','post'])
def add_election():
    session['head'] = "add election"
    if session['lg'] == "lin":
        if request.method=="POST":
            election_name=request.form['textfield']
            election_year= request.form['textfield2']

            db=Db()
            db.insert("insert into election values('','"+election_name+"','"+election_year+"','pending')")
            return '<script>alert("Added successfully");window.location="/view_election"</script>'
        else:
         return render_template('admin/add election.html')
    else:
        return redirect('/')
@app.route('/add_notification',methods=['get','post'])
def add_notification():
    session['head'] = "add notification"
    if session['lg'] == "lin":
        if request.method=="POST":
          election_name=request.form['select']
          title=request.form['textfield']
          content=request.form['textarea']
          db=Db()
          db.insert("insert into notification values('',curdate(),'"+title+"','"+content+"','"+election_name+"')")
          return '<script>alert("added successfully");window.location="/add_notification"</script>'
        else:
            db=Db()
            res=db.select("select * from election")
            return render_template('admin/add notification.html',data=res)
    else:
        return redirect('/')
@app.route('/add_post/<eid>',methods=['get','post'])
def add_post(eid):
    session['head'] = "add post"
    if session['lg'] == "lin":
        if request.method == "POST":
            post_name = request.form['textfield']
            db=Db()
            db.insert("insert into post values('','"+post_name+"','"+eid+"')")
            return '<script>alert("successfully inserted");window.location="/view_election#a"</script>'
        else:
            db=Db()
            res=db.select("select * from post where election_id='"+eid+"'")
            return render_template('admin/add post.html',data=res)
    else:
        return redirect('/')

@app.route('/delete_post/<pid>')
def delete_post(pid):
    session['head'] = "delete post"
    if session['lg'] == "lin":
        db=Db()
        db.delete("delete from post where post_id='"+pid+"'")
        return '<script>alert("deleted successfully");window.location="/view_election#a"</script>'
    else:
        return redirect('/')




# @app.route('/add_student',methods=['get','post'])
# def add_student():
#     if session['lg'] == "lin":
#         if request.method=="POST":
#             name=request.form['textfield']
#             Email=request.form['textfield2']
#             Phone=request.form['textfield3']
#             Course=request.form['select']
#             Semester=request.form['select2']
#             Batch=request.form['select3']
#             db=Db()
#             db.insert("insert into student values('','"+name+"','"+Email+"','"+Phone+"','"+Course+"','"+Semester+"','"+Batch+"')")
#             return '<script>alert("successfully added");window.location="/"</script>'
#         else:
#             db = Db()
#             res = db.select("select * from course")
#             return render_template('admin/add student.html',data=res)
#     else:
#         return redirect('/')

@app.route('/add_department',methods=['get','post'])
def add_department():
    session['head'] = "add department"
    if session['lg'] == "lin":
        if request.method=="POST":
           dn=request.form['textfield']
           db = Db()
           db.insert("insert into department values('','"+dn+"')")
           return '<script>alert("added successfully");window.location="/add_department"</script>'
        else:
           return render_template('admin/add_department.html')
    else:
        return redirect('/')


@app.route('/change_password',methods=['get','post'])
def change_password():
    session['head'] = "change password"
    if session['lg'] == "lin":
        if request.method == "POST":
             old_password = request.form['textfield3']
             new_password = request.form['textfield']
             confirm_password = request.form['textfield2']
             db = Db()
             res=db.selectOne("select * from login where password='"+old_password+"' and usertype='admin'")
             if res is not None:
                 if new_password==confirm_password:
                     db=Db()
                     db.update("update login set password='"+confirm_password+"' where usertype='admin'")
                     return '<script>alert("password change successfully");window.location="/change_password"</script>'
                 else:
                     return '<script>alert("password mismatch");window.location="/change_password"</script>'
             else:
                 return '<script>alert("Invalid old password");window.location="/change_password"</script>'
        else:
            return render_template('admin/change password.html')
    else:
        return redirect('/')

@app.route('/approve_candidate')
def approve_candidate ():
    session['head'] = "approve candidates"
    if session['lg'] == "lin":
        db = Db()
        res = db.select("select * from candidate,student where candidate.student_id=student.student_id ")
        return render_template('admin/approve candidates.html',data=res)
    else:
        return redirect('/')

@app.route('/edit_course/<cid>',methods=['get','post'])
def edit_course(cid):
    session['head'] = "edit course"
    if session['lg'] == "lin":

        if request.method == "POST":
            department = request.form['select']
            course_name= request.form['textfield']
            db = Db()
            db.update("update course set dep_id='" + department + "', course_name='" + course_name + "' where course_id='"+cid+"' ")
            return '<script>alert("Edited Successfully");window.location="/view_department"</script>'
        else:
            db = Db()
            res = db.selectOne("select * from course where course_id='"+cid+"'")
            res2=db.select("select * from department")
            return render_template('admin/edit course.html',data=res,data2=res2)
    else:
        return (redirect('/'))

@app.route('/edit_election/<eid>',methods=['get','post'])
def edit_election (eid):
    session['head'] = "edit election"
    if session['lg'] == "lin":
        if request.method == "POST":
            election_name = request.form['textfield']
            year = request.form['textfield2']
            db = Db()
            db.update("update election set election_name='" + election_name + "', election_year='" + year + "' where election_id='"+eid+"' ")
            return '<script>alert("Edited Successfully");window.location="/edit_department"</script>'
        else:
            db = Db()
            res = db.selectOne("select * from election where election_id='" + eid + "'")
            return render_template('admin/edit election.html',data=res)
    else:
        return redirect('/')

@app.route('/edit_student/<sid>',methods=['get','post'])
def edit_student (sid):
    session['head'] = "edit student"
    if session['lg'] == "lin":
        if request.method == "POST":
            name = request.form['textfield']
            email = request.form['textfield2']
            phone = request.form['textfield3']
            course = request.form['select']
            semester = request.form['select2']
            batch=request.form['select3']
            db = Db()
            db.update("update student set name='" + name + "', email='" + email + "',phone='"+phone+"',course_id='"+course+"',semester='"+semester+"',batch='"+batch+"'where student_id='" + sid + "'")
            return '<script>alert("Edited Successfully");window.location="/view_student#a"</script>'
        else:
            db = Db()
            res = db.selectOne("select * from student where student_id='" + sid + "'")
            res1 = db.select("select * from course")
            return render_template('admin/edit student.html',data=res,data1=res1)
    else:
        return redirect('/')


@app.route('/view_course')
def view_course ():
    session['head'] = "view course"
    if session['lg'] == "lin":
        db = Db()
        res = db.select("select * from course,department where course.dep_id=department.dep_id")
        return render_template('admin/view course.html',data=res)
    else:
        return redirect('/')

@app.route('/delete_course/<cid>')
def delete_course(cid):
    session['head'] = "delete course"
    if session['lg'] == "lin":
        db=Db()
        db.delete("delete from course where course_id='"+cid+"'")
        return '<script>alert("deleted successfully");window.location="/view_course"</script>'
    else:
        return redirect('/')

@app.route('/view_department')
def view_department():
    if session['lg'] == "lin":
        db=Db()
        res=db.select("select * from department")
        return render_template('admin/view department.html',data=res)
    else:
        return redirect('/')

@app.route('/delete_department/<did>')
def delete_department(did):
    session['head'] = "delete department"
    if session['lg'] == "lin":
        db=Db()
        db.delete("delete from department where dep_id='"+did+"'")
        return '<script>alert("deleted successfully");window.location="/view_department"</script>'
    else:
        return redirect('/')

@app.route('/view_election')
def view_election():
    session['head'] = "view election"
    if session['lg'] == "lin":
        db=Db()
        res=db.select("select * from election")
        return render_template('admin/view election.html',data=res)
    else:
        return redirect('/')

@app.route('/publish_result/<i>')
def publish_result(i):
    session['head'] = "publish result"
    if session['lg'] == "lin":
        db=Db()
        res=db.update("update election set status='published'where election_id='"+i+"'")
        return '<script>alert("published successfully");window.location="/view_election"</script>'
    else:
        return redirect('/')
@app.route('/delete_election/<eid>')
def delete_election(eid):
    session['head'] = "delete election"
    if session['lg'] == "lin":
        db=Db()
        db.delete("delete from election where election_id='"+eid+"'")
        return '<script>alert("deleted successfully");window.location="/view_election"</script>'
    else:
        return redirect('/')


@app.route('/view_live_result/<eid>',methods=['get','post'])
def view_live_result (eid):
    session['head'] = "view live result"
    if session['lg'] == "lin":
        if request.method=="POST":
            # election=request.form['select']

            post=request.form['select2']
            db=Db()
            res=db.select("SELECT `student`.name, `candidate`.party, candidate.symbol, COUNT(voting.vote_id) AS votes FROM `voting`, `candidate`, `student` WHERE `voting`.candidate_id=`candidate`.candidate_id AND `candidate`.student_id=`student`.student_id AND `candidate`.post_id='"+post+"' GROUP BY `candidate`.candidate_id")
            # res1=db.select("select * from election")
            res2=db.select("select * from post where election_id='"+eid+"'")
            return render_template('admin/view live result.html',data=res ,data2=res2)
        else:
            db=Db()
            # res=db.select("SELECT * FROM result,candidate,post,student,election WHERE candidate.candidate_id=result.candidate_id AND candidate.post_id=post.post_id AND post.election_id=election.election_id AND candidate.student_id=student.student_id")
            # res1=db.select("select * from election")
            res2=db.select("select * from post where election_id='"+eid+"'")
            return render_template('admin/view live result.html',data2=res2)
    else:
        return redirect('/')

@app.route('/view_notification')
def view_notification ():
    session['head'] = "view notification"
    if session['lg'] == "lin":
        db = Db()
        res = db.select("SELECT * FROM `notification`,`election` WHERE `notification`.`election_id`=`election`.`election_id`")
        return render_template('admin/view notification.html',data=res)
    else:
        return redirect('/')


@app.route('/delete_notification/<nid>')
def delete_notification(nid):
    session['head'] = "delete notification"
    if session['lg'] == "lin":
        db=Db()
        db.delete("delete from notification where notification_id='"+nid+"'")
        return '<script>alert("deleted successfully");window.location="/view_notification"</script>'
    else:
        return redirect('/')

@app.route('/view_student')
def view_student ():
    session['head'] = "view student"
    if session['lg'] == "lin":
        db=Db()
        res=db.select("select * from student,course where course.course_id=student.course_id")
        return render_template('admin/view student.html',data=res)
    else:
        return redirect('/')

@app.route('/delete_student/<sid>')
def delete_student(sid):
    session['head'] = "delete student"
    db=Db()
    db.delete("delete from student where student_id='"+sid+"'")
    return '<script>alert("deleted successfully");window.location="/view_student"</script>'



@app.route('/view_post')
def view_post ():
    session['head'] = "view post"
    if session['lg']=="lin":
     db = Db()
     res = db.select("SELECT * FROM post,election where post.election_id=election.election_id")
     return render_template('admin/view post.html',data=res)
    else: return redirect('/')

@app.route('/view_applied_candidates/<pid>')
def view_applied_candidates (pid):
    session['head'] = "view applied candidates"
    if session['lg'] == "lin":
        db = Db()
        res = db.select("select * from candidate,post,student where candidate.post_id=post.post_id and candidate.student_id=student.student_id and candidate.status='pending' and candidate.post_id='"+pid+"'")
        return render_template('admin/view applied candidates.html',data=res)
    else:
        return redirect('/')

@app.route('/approve_candidates/<cid>',methods=['get','post'])
def approve_candidates (cid):
    session['head'] = "approval submission"
    if session['lg'] == "lin":
        if request.method == "POST":
            em = request.form['textfield']
            p=random.randint(0000,9999)
            db = Db()
            qry=db.select("select * from student")

            if qry is not None:
                try:
                    gmail = smtplib.SMTP('smtp.gmail.com', 587)

                    gmail.ehlo()

                    gmail.starttls()

                    gmail.login('snehachandran300@gmail.com', "zkjhftaqkvbhonhw")

                except Exception as e:
                    print("Couldn't setup email!!" + str(em))

                msg = MIMEText("Your Password is " + str(p))

                msg['Subject'] = 'Verification'

                msg['To'] = em

                msg['From'] = 'snehachandran300@gmail.com'

                try:

                    gmail.send_message(msg)

                except Exception as e:

                    print("COULDN'T SEND EMAIL", str(em))
            # return '''<script>alert("Mail Send successfully");window.location='/'</script>'''

            db.update("update login set usertype='candidate'  , password='"+str(p)+"' where login_id='"+cid+"'")
            db.update("update candidate set status='approved' where candidate_id='" + cid + "'")
            return '<script>alert("successfull");window.location="/view_post"</script>'


        else:
            return render_template('candidate/submit.html')
    else:
        return redirect('/')


@app.route('/reject_candidates/<cid>')
def reject_candidates (cid):
    session['head'] = "view rejected candidates"
    if session['lg'] == "lin":
        db = Db()
        db.update("update candidate set status='rejected'where candidate_id='" + cid + "'")
        return '<script>alert("rejected");window.location="/view_post"</script>'
    else:
        return redirect('/')

@app.route('/logout')
def logout ():
    db=Db()
    session.clear()
    session['lg']=""
    return redirect('/')
###################student###########
@app.route('/add_student',methods=['get','post'])
def register():
        if request.method=="POST":
            name=request.form['textfield']
            Email=request.form['textfield2']
            Phone=request.form['textfield3']
            Course=request.form['select']
            Semester=request.form['select2']
            Batch=request.form['select3']
            password=request.form['textfield13']
            db=Db()
            res=db.insert("insert into login values ('','"+name+"','"+password+"','student')")
            db.insert("insert into student values('"+str(res)+"','"+name+"','"+Email+"','"+Phone+"','"+Course+"','"+Semester+"','"+Batch+"')")
            return '<script>alert("successfully registered");window.location="/"</script>'
        else:
            db = Db()
            res = db.select("select * from course")
            return render_template("regindex.html",data=res)

@app.route('/student_home')
def student_home():

    return render_template('student/studentindex.html')




@app.route('/view_profile',methods=['get','post'])
def view_profile():
    session['head'] = "view profile"

    if session['lg'] == "lin":
        db=Db()
        res=db.selectOne("select * from student,course where course.course_id=student.course_id  and student.student_id='"+str(session['lid'])+"'")
        return render_template("student/view_profile.html",data=res)
    else:
        return redirect('/')

@app.route('/view_notifications')
def view_notifications():
    session['head'] = "view notification"
    if session['lg'] == "lin":
        db=Db()
        res=db.select("select * from notification,election where election.election_id=notification.election_id")
        return render_template("student/view notification.html",data=res)
    else:
        return redirect('/')


@app.route('/view_elections')
def view_elections():
    session['head'] = "view election"
    if session['lg'] == "lin":
        db=Db()
        res=db.select("select * from election where status='pending'")
        return render_template("student/view election.html",data=res)
    else:
        return redirect('/')



@app.route('/view_posts/<eid>')
def view_posts(eid):
    session['head'] = "view post"

    if session['lg'] == "lin":
        db=Db()
        res=db.select("select * from post,election where post.election_id=election.election_id and post.election_id='"+eid+"'")
        return render_template("student/view post.html",data=res)
    else:
        return redirect('/')

@app.route('/post_apply/<pid>',methods=['get','post'])
def post_apply(pid):
    session['head'] = "post apply"
    if session['lg'] == "lin":
       if request.method == "POST":
            party = request.form['select']
            symbol = request.files['fileField']
            db=Db()
            date=datetime.datetime.now().strftime("%y%m%d-%%H%M%S")
            symbol.save(r"C:\Users\user\PycharmProjects\online  voting\static\symbol\\"+date+'.jpg')
            p="/static/symbol/"+date+'.jpg'
            q=db.insert("insert into login VALUES ('','" + str(session['e']) + "','pending','pending')")
            db.insert("insert into candidate values('"+str(q)+"','"+pid+"','"+str(session['lid'])+"','" + party + "','pending','" + str(p) + "')")
            return '<script>alert("successfull");window.location="/view_elections"</script>'
       else:
        return render_template('student/apply.html')
    else:
        return redirect('/')


@app.route('/vote1',methods=['get','post'])
def vote1():
    session['head'] = "voting"
    if session['lg'] == "lin":
        if request.method=="POST":
            post=request.form['select2']
            db=Db()
            res3 = db.select("select * from election")
            res=db.select("select * from post,election where post.election_id=election.election_id and election.election_id='"+post+"' ")
            print("select * from post,election where post.election_id=election.election_id and election.election_id='"+post+"'")
            return render_template("student/vote1.html", data1=res,data3=res3)
        else:
            db=Db()
            res3=db.select("select * from election")
            res2 = db.select("select * from post,election where post.election_id=election.election_id")
            return render_template("student/vote1.html", data1=res2, data3=res3)

    return redirect('/')

@app.route('/vote2/<vid>')
def vote2(vid):
    session['head'] = "voting"
    if session['lg'] == "lin":
       db=Db()
       res=db.select("select * from candidate,student where candidate.student_id=student.student_id and post_id='" + vid + "'")

       return render_template("student/vote2.html", data=res)
    else:
       return redirect('/')

@app.route('/vote3/<vid>')
def vote3(vid):
    if session['lg'] == "lin":
       db=Db()
       res=db.selectOne("select * from voting where student_id='"+str(session['lid'])+"'  ")
       if res is not None:
           return '<script>alert("already voted");window.location="/vote1"</script>'
       else:
        db.insert("insert into voting values('','"+vid+"','"+str(session['lid'])+"') ")
        return '<script>alert("successfully voted");window.location="/vote1"</script>'

    else:
       return redirect('/')

@app.route('/view_live_results',methods=['get','post'])
def view_live_results():
    session['head'] = "result"
    if session['lg'] == "lin":
        if request.method=="POST":

            election=request.form['select']
            post=request.form['select2']
            db=Db()
            res2 = db.select("select * from post")
            res1 = db.select("select * from election")
            res=db.select("SELECT  voting.*,candidate.*,post.*,student.*,election.*,COUNT(`voting`.`candidate_id`) as c,`election`.`status` AS es FROM voting,candidate,post,student,election WHERE candidate.candidate_id=voting.candidate_id AND candidate.post_id=post.post_id AND post.election_id=election.election_id AND candidate.student_id=student.student_id AND post.post_id='"+post+"' AND election.election_id='"+election+"'")
            result=[]
            for i in res:
                if i['vote_id'] != '' and i['es'] == 'published':

                    result.append(i)
            if len(result)>0:
                return render_template('student/view live results.html',data=result,data1=res1,data2=res2)
            else:
                return render_template('student/view live results.html',data1=res1,data2=res2)
        else:
            db=Db()
            res1=db.select("select * from election")
            res2=db.select("select * from post")
            return render_template('student/view live results.html',data1=res1,data2=res2)
    else:
        return redirect('/')

def edit_students (sid):
    session['head'] = "edit student"
    if session['lg'] == "lin":
        if request.method == "POST":
            name = request.form['textfield']
            email = request.form['textfield2']
            phone = request.form['textfield3']
            course = request.form['select']
            semester = request.form['select2']
            batch=request.form['select3']
            db = Db()
            db.update("update student set name='" + name + "', email='" + email + "',phone='"+phone+"',course_id='"+course+"',semester='"+semester+"',batch='"+batch+"'where student_id='" + sid + "'")
            return "ok"
        else:
            db = Db()
            res = db.selectOne("select * from student where student_id='" + sid + "'")
            res1 = db.select("select * from course")
            return render_template('candidate/edit student.html',data=res,data1=res1)
    else:
        return redirect('/')




@app.route('/change_passwords',methods=['get','post'])
def change_passwords():
    session['head'] = "change password"
    if session['lg'] == "lin":

        if request.method == "POST":
             old_password = request.form['textfield3']
             new_password = request.form['textfield']
             confirm_password = request.form['textfield2']
             db = Db()
             res=db.selectOne("select * from login where password='"+old_password+"' and login_id='"+str(session['lid'])+"'")
             if res is not None:
                if new_password==confirm_password:
                     db=Db()
                     db.update("update login set password='"+confirm_password+"' where login_id='"+str(session['lid'])+"'")
                     return '<script>alert("password change successfully");window.location="/change_passwords"</script>'
                else:
                     return '<script>alert("password mismatch");window.location="/change_passwords"</script>'
             else:
                  return '<script>alert("Invalid old password");window.location="/change_passwords"</script>'
        else:
            return render_template('student/change password.html')
    else:
        return redirect('/')

###################candidate###########



@app.route('/candidate_home')
def candidate_home():

    return render_template('candidate/candidateindex.html')


@app.route('/view_profiles',methods=['get','post'])
def view_profiles():
    session['head'] = "view profile"
    if session['lg'] == "lin":
        db=Db()
        res=db.selectOne("select * from student,candidate where student.student_id=candidate.student_id and candidate.candidate_id='"+str(session['lid'])+"' ")
        return render_template("candidate/view profile.html",data=res)
    else:
        return redirect('/')



@app.route('/view_postss')
def view_postss():
    session['head'] = "view post"
    if session['lg'] == "lin":
        db=Db()
        res=db.select("select * from post,election where post.election_id=election.election_id ")
        return render_template("candidate/view post.html",data=res)
    else:
        return redirect('/')


@app.route('/view_applied_candidatess/<pid>')
def view_applied_candidatess (pid):
    session['head'] = "view candidate"

    if session['lg'] == "lin":
        db = Db()
        res = db.select("select * from candidate,student where candidate.student_id=student.student_id and candidate.post_id='"+pid+"'")
        return render_template('candidate/view applied candidates.html',data=res)
    else:
        return redirect('/')




@app.route('/view_live_resultss',methods=['get','post'])
def view_live_resultss():
    session['head'] = "view live result"
    if session['lg'] == "lin":
        if request.method == "POST":

            election = request.form['select']
            post = request.form['select2']
            db = Db()
            res2 = db.select("select * from post")
            res1 = db.select("select * from election")
            res = db.select(
                "SELECT  voting.*,candidate.*,post.*,student.*,election.*,COUNT(`voting`.`candidate_id`) as c,`election`.`status` AS es FROM voting,candidate,post,student,election WHERE candidate.candidate_id=voting.candidate_id AND candidate.post_id=post.post_id AND post.election_id=election.election_id AND candidate.student_id=student.student_id AND post.post_id='" + post + "' AND election.election_id='" + election + "'")
            result = []
            for i in res:
                if i['vote_id'] != '' and i['es'] == 'published':
                    result.append(i)
            if len(result) > 0:
                return render_template('student/view live results.html', data=result, data1=res1, data2=res2)
            else:
                return render_template('student/view live results.html', data1=res1, data2=res2)
        else:
            db = Db()
            res1 = db.select("select * from election")
            res2 = db.select("select * from post")
            return render_template('student/view live results.html', data1=res1, data2=res2)
    else:
        return redirect('/')



@app.route('/change_passwordss',methods=['get','post'])
def change_passwordss():
    session['head'] = "change password"
    if session['lg'] == "lin":
        if request.method == "POST":
             old_password = request.form['textfield3']
             new_password = request.form['textfield']
             confirm_password = request.form['textfield2']
             db = Db()
             res=db.selectOne("select * from login where password='"+old_password+"' and login_id='"+str(session['lid'])+"'")
             if res is not None:
                if new_password==confirm_password:
                     db=Db()
                     db.update("update login set password='"+confirm_password+"' where login_id='"+str(session['lid'])+"'")
                     return '<script>alert("password change successfully");window.location="/change_passwordss"</script>'
                else:
                     return '<script>alert("password mismatch");window.location="/change_passwordss"</script>'
             else:
                  return '<script>alert("Invalid old password");window.location="/change_passwordss"</script>'
        else:
            return render_template('candidate/change password.html')
    else:
        return redirect('/')
##############################

if __name__ == '__main__':
    app.run(port=5000)
