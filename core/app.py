"""
This Python file contains Flask APP Code By Mobasa Tech
"""
# -----------------------------------------------------------
import datetime
import os
import random
import string
from uuid import uuid4
from flask import *  # import all from flask library
import pymongo
import certifi
import gridfs
from bson import json_util, objectid
from PIL import Image
import io
from flask_cors import CORS
import base64
import re
# -----------------------------------------------------------------
# ca = certifi.where()
# client = pymongo.MongoClient(os.getenv('mongoDB_string'), tlsCAFile=ca)
# db=client['projects']
# col=db['project_details']
# team_col=db['staff_details']
# test_col=db['testimonial_data']
# fs=gridfs.GridFS(db)
# ----------------------------------------------------------------
#template_dir = os.path.abspath('../templates')
app = Flask(__name__)  # initialize the flask app to app
CORS(app)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
# ---------------------------------------------#
temp_files = {}
# ---------------------------------------------#


def serve_pil_image(pil_img):
    img_io = io.BytesIO()
    pil_img.save(img_io, 'JPEG', quality=50)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


active_tokens = []


def Generate_Token():
    token = str(uuid4())
    if token not in active_tokens:
        active_tokens.append(token)
        return token
    return Generate_Token()


# ------------------------------------------------------------
"""
HTTP error Handling Code
"""
# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template('error.html',errormsg="Page Not Found",errorcode=404), 404

# @app.errorhandler(500)
# def internal_server_error(e):
#     # note that we set the 500 status explicitly
#     return render_template('error.html',errormsg="We Seem To Have Made A Mistake, Sorry!",errorcode=500), 500
# @app.errorhandler(405)
# def method_not_allowed(e):
#     return render_template('error.html', errormsg="Method Not Allowed", errorcode=405), 405
# ----------------------------------------------------------
"""
This routes are publically accessable
"""


@app.route('/')  # index url
def index():
    # projects = col.find({})
    # projects_json = json.loads(json_util.dumps(projects))
    # testimonials=json.loads(json_util.dumps(test_col.find({"status":1})))
    # it renders index.html from templates folder
    return render_template('index.html')

# @app.route('/projects/')#projects url
# def projects():
#     projects=col.find({})
#     projects_json=json.loads(json_util.dumps(projects))
#     return render_template('projects.html',projects=projects_json)
# @app.route("/aboutus/")#about us url
# def aboutus():
#     return render_template('about.html')

# @app.route("/team") #team url
# def team():
#     team_members=team_col.find({})
#     team_members=json.loads(json_util.dumps(team_members))
#     return render_template('team.html',team_members=team_members)

# @app.route("/testimonials/")#separate page testimonials url
# def testimonials():
#     testimonials=json.loads(json_util.dumps(test_col.find({"status":1})))
#     return render_template('testimonials.html',testimonials=testimonials)
# @app.route("/faq/")#faq url
# def faq():
#     return render_template('faq.html')
# @app.route("/services/")#services url
# def services():
#     return render_template('services.html')
# @app.route('/contact/')#contact url
# def contact():
#     return render_template('contact.html')

# @app.route('/view-project/',methods=['GET'])#view individual projects url
# def view_project():
#     id=int(request.args.get('id'))
#     project_details=col.find_one({'project_id':id})
#     return render_template('projects-single.html',project=json.loads(json_util.dumps(project_details)))

# @app.get('/Get-Img/<id>/')#this url for all images
# def getimg(id:str):
#     try:
#         file=fs.get(objectid.ObjectId(id))
#         buffer = io.BytesIO()
#         for data in file:
#             buffer.write(data)
#         buffer.seek(0)
#         img = Image.open(buffer)
#         return serve_pil_image(img)
#     except Exception as e:
#         return {'status':False,'msg':'Error Occured','error':str(e)}
# #---------------------------------------------------------------------
# """
# these are project accessable only by admin with password
# """
# @app.route('/login/',methods=['POST','GET']) #login url
# def login():
#     if request.method=='POST':
#         login_data=json.loads(request.data)
#         if login_data['username']=='admin' and login_data['password']=='admin@7878':
#             return {"status":True,"msg":"Login Done","token":Generate_Token()}
#         else:
#             return {"status":False,"msg":"Credentials Incorrect"}
#     else:
#         msg=request.args.get('msg')
#         return render_template('login.html',msg=msg)
# @app.route('/dashboard/') #dashboard url
# def dashboard():
#     projects = col.find({})
#     projects_json = json.loads(json_util.dumps(projects))
#     team_members = team_col.find({})
#     team_members = json.loads(json_util.dumps(team_members))
#     testimonials= test_col.find({})
#     testimonials = json.loads(json_util.dumps(testimonials))
#     return render_template('dashboard.html',projects=projects_json,team_members=team_members,testimonials=testimonials)

# #----------------------------------------------------------------
# """
# these are used to stored images in runtime storage which is used to store in mongoDB later
# """
# @app.route('/uploadtemp/<token>',methods=['GET','POST'])#images push api
# def uploadtemp(token):
#     if token not in active_tokens:
#         return {"status":False,"cat":"logout","msg":"NO ACCESS PLEASE LOGIN AGAIN"}
#     if request.method=='POST':
#         try:
#             file=json.loads(request.data)
#             base64_data = re.sub('^data:image/.+;base64,', '', file['img'])
#             im = Image.open(io.BytesIO(base64.b64decode(base64_data)))
#             im=im.resize((750,600))
#             im=im.convert('RGB')
#             if file['project_temp_id'] not in temp_files:
#                 temp_files[file['project_temp_id']]={}
#                 temp_files[file['project_temp_id']][file['id']]=im
#             else:
#                 temp_files [ file [ 'project_temp_id' ] ] [ file [ 'id' ] ]=im
#         except Exception as e:
#             return {"status":False,"msg":"Error occured","error":str(e),"cat":"img"}
#         return {"status":True,"msg":"files are uploaded in temp","cat":"img"}
#     else:
#         return {"status":False,"msg":"Method not allowed","cat":"img"}
# @app.route('/removetemp/<token>',methods=["POST","GET"])#images remove api
# def removetemp(token):
#     if token not in active_tokens:
#         return {"status":False,"cat":"logout","msg":"NO ACCESS PLEASE LOGIN AGAIN"}
#     try:
#         if request.method=="POST":
#             file=json.loads(request.data)
#             if file['mode']:
#                 fs.delete(objectid.ObjectId(file['img_id']))
#                 col.update_one({"project_id":int(file['project_id'])},{"$pull":{"project_main_imgs":file['img_id']}})
#                 return {"status": True, "msg": "image removed", "cat": "remove","id":file['img_id']}
#             if file['img_id'] in temp_files:
#                 temp_files[file['project_temp_id']].pop(file['img_id'])
#                 return {"status":True,"msg":"image removed","cat":"remove"}
#             return {"status":True,"msg":"image not found","cat":"remove"}
#         return {"status":False,"msg":"method not allowed","cat":"remove"}
#     except Exception as e:
#         return {"status": False, "msg": "Error Occured and prevented from crash", "error": str(e), "cat": "error"}
# #----------------------------------------------------------------
# """
# these apis are used manuplate the projects section
# """
# @app.route('/AddProject/<token>/',methods=['POST','GET'])#add project api
# def add_project(token):
#     if token not in active_tokens:
#         return {"status":False,"cat":"logout","msg":"NO ACCESS PLEASE LOGIN AGAIN"}
#     global temp_files
#     try:
#         if request.method=='POST':
#             FormData=json.loads(request.data)
#             img_ids = [ ]
#             for img in temp_files [FormData['project_temp_id']].values():
#                 curpath = os.getcwd()
#                 curpath += "/static/images/projects/tempproject.jpg"
#                 img.save(curpath)
#                 with open(curpath, 'rb') as f:
#                     content = f.read()
#                 file = fs.put(content, filename=''.join(random.choices(string.ascii_letters+string.digits, k=5))+'.jpg')
#                 img_ids.append(str(file))
#                 os.remove(curpath)
#             if col.find_one(sort=[ ("project_id", -1) ]) == None:
#                 p_id = 1
#             else:
#                 p_id = col.find_one(sort=[ ("project_id", -1) ]) [ 'project_id' ]+1
#             project = { 'project_id': p_id, 'project_title': FormData['project_title'],
#                         'project_main_imgs': img_ids, 'project_decription': FormData['project_des'].split('\n'),'project_cat':FormData['project_cat']}
#                         #'project_start_date': FormData['start_date'], 'project_end_date': FormData['end_date'], 'updated_date': str(datetime.datetime.today()),'project_cat': FormData['project_cat']
#                         #'updated_staff_name': FormData['updated_by'], 'project_owner': FormData['client'], 'project_address': FormData['address'], 'project_assigned_staff':FormData['assigned_staff'] , 'project_amount': FormData['project_amount']}
#             col.insert_one(project)
#             temp_files={}
#             project=json.loads(json_util.dumps(project))
#             project['cat']='add'
#             project['status']=True
#             return project
#         else:
#             return {"status":False,"msg":"This method not allowed"}
#     except Exception as e:
#         return {"status": False, "msg": "Error Occured and prevented from crash", "error": str(e), "cat": "error"}
# @app.route('/editproject/<id>/<token>/',methods=['GET','POST']) #edit project api
# def editproject(id,token):
#     if token not in active_tokens:
#         return {"status":False,"cat":"logout","msg":"NO ACCESS PLEASE LOGIN AGAIN"}
#     try:
#         if request.method=='GET':
#             id=int(id)
#             project_det=col.find_one({"project_id":id})
#             project_det=json.loads(json_util.dumps(project_det))
#             return project_det
#         else:
#             global temp_files
#             img_ids = [ ]
#             id=int(id)
#             if str(id) in temp_files:
#                 for img in temp_files[str(id)].values():
#                     curpath = os.getcwd()
#                     curpath += "/static/images/projects/tempproject.jpg"
#                     img.save(curpath)
#                     with open(curpath, 'rb') as f:
#                         content = f.read()
#                     file = fs.put(content, filename=''.join(random.choices(string.ascii_letters+string.digits, k=5))+'.jpg')
#                     img_ids.append(str(file))
#                     os.remove(curpath)
#             FormData = json.loads(request.data)
#             col.update_one({'project_id':id},{"$set":{'project_title': FormData['project_title'],
#                          'project_decription': FormData['project_des'].split('\n'),'project_cat':FormData['project_cat']}})
#             col.update_one({'project_id':id},{"$push":{'project_main_imgs':{"$each": img_ids}}})
#             temp_files = {}
#             project = json.loads(json_util.dumps(col.find_one({"project_id":id})))
#             project [ 'cat' ] = 'edit'
#             project [ 'status' ] = True
#             return project
#     except Exception as e:
#         return {"status": False, "msg": "Error Occured and prevented from crash", "error": str(e), "cat": "error"}

# @app.route('/RemoveProject/<id>/<cat>/<token>/',methods=['GET'])#api remove project and employee data from DB
# def removeproject(id,cat,token):
#     if token not in active_tokens:
#         return {"status":False,"cat":"logout","msg":"NO ACCESS PLEASE LOGIN AGAIN"}
#     try:
#         id = int(id)
#         if cat=="project":
#             prject=col.find_one({'project_id':id})
#             for img in prject['project_main_imgs']:
#                 fs.delete(objectid.ObjectId(img))
#             col.delete_one({"project_id":id})
#             return {"status":True,"msg":f"Project-{id} removed successfully",'project_id':id,"cat":"project"}
#         elif cat=="emp":
#             emp = team_col.find_one({'emp_id': id})
#             fs.delete(objectid.ObjectId(emp['emp_img']))
#             team_col.delete_one({"emp_id": id})
#             return {"status": True, "msg": f"emp-{id} removed successfully", 'emp_id': id,"cat":"emp"}
#         else:
#             return {"status": False, "msg": f"emp-{id} not removed successfully (category incorrect)","cat":'error'}
#     except Exception as e:
#         return {"status":False,"msg":"Error Occured and prevented from crash","error":str(e),"cat":"error"}
# #----------------------------------------------------------------
# """"
# These apis are used to manipulate team members data
# """
# @app.route('/addmember/<token>',methods=['POST']) #add member api
# def addmember(token):
#     if token not in active_tokens:
#         return {"status":False,"cat":"logout","msg":"NO ACCESS PLEASE LOGIN AGAIN"}
#     try:
#         if request.method=='POST':
#             staff_form_data=json.loads(request.data)
#             if staff_form_data['savetype']=='true':
#                 if '/Get-Img/' not in staff_form_data['file']:
#                     base64_data = re.sub('^data:image/.+;base64,', '', staff_form_data [ 'file' ])
#                     im = Image.open(io.BytesIO(base64.b64decode(base64_data)))
#                     im = im.resize((260, 300))
#                     im = im.convert('RGB')
#                     curpath = os.getcwd()
#                     curpath += "/static/images/team/tempimg.jpg"
#                     im.save(curpath, 'JPEG', quality=50)
#                     with open(curpath, 'rb') as f:
#                         content = f.read()
#                     file = fs.put(content, filename=''.join(random.choices(string.ascii_letters+string.digits, k=5))+'.jpg')
#                     os.remove(curpath)
#                 else:
#                     file=staff_form_data['file'].split('/')[-1]
#                 emp_id=staff_form_data['emp_id']
#                 team_col.update_one({'emp_id': int(emp_id)}, {"$set": {
#                     "emp_name": staff_form_data [ 'emp-name' ],
#                     "emp_img": str(file),
#                     "emp_designation": staff_form_data [ 'emp-desig' ],
#                     "emp_description": staff_form_data [ 'emp-description' ],
#                     "emp_mobile": staff_form_data [ 'con-phone' ],
#                     "emp_facebook": staff_form_data [ 'con-facebook' ],
#                     "emp_twitter": staff_form_data [ "con-twitter" ],
#                     "emp_linkedin": staff_form_data [ 'con-linkedin' ],
#                     "emp_email": staff_form_data [ 'con-email' ]}})
#                 new_emp_det = json.loads(json_util.dumps(team_col.find_one({"emp_id": int(emp_id)})))
#                 new_emp_det [ 'cat' ] = 'empedit'
#                 new_emp_det [ 'status' ] = True
#                 return new_emp_det
#             base64_data = re.sub('^data:image/.+;base64,', '', staff_form_data [ 'file' ])
#             im = Image.open(io.BytesIO(base64.b64decode(base64_data)))
#             im = im.resize((260, 300))
#             im = im.convert('RGB')
#             curpath = os.getcwd()
#             curpath += "/static/images/team/tempimg.jpg"
#             im.save(curpath,'JPEG', quality=50)
#             with open(curpath, 'rb') as f:
#                 content = f.read()
#             file = fs.put(content, filename=''.join(random.choices(string.ascii_letters+string.digits, k=5))+'.jpg')
#             os.remove(curpath)
#             if team_col.find_one(sort=[ ("emp_id", -1) ]) == None:
#                 emp_id = 1
#             else:
#                 emp_id = team_col.find_one(sort=[ ("emp_id", -1) ]) [ 'emp_id' ]+1
#             staff_data={"emp_id":emp_id,
#                         "emp_name":staff_form_data['emp-name'],
#                         "emp_img":str(file),
#                         "emp_designation":staff_form_data['emp-desig'],
#                         "emp_description":staff_form_data['emp-description'],
#                         "emp_mobile":staff_form_data['con-phone'],
#                         "emp_facebook":staff_form_data['con-facebook'],
#                         "emp_twitter":staff_form_data["con-twitter"],
#                         "emp_linkedin":staff_form_data['con-linkedin'],
#                         "emp_email":staff_form_data['con-email']}
#             team_col.insert_one(staff_data)
#             staff_data= json.loads(json_util.dumps(staff_data))
#             staff_data['cat']='empadd'
#             staff_data['status']=True
#             return staff_data
#         return {"status": False, "msg": "method not allowed"}
#     except Exception as e:
#         return {"status": False, "msg": "Error Occured From Server Side", "error": str(e)}
# @app.route("/editemp/<id>/<token>/",methods=['GET']) #edit employee details api
# def editemp(id,token):
#     if token not in active_tokens:
#         return {"status":False,"cat":"logout","msg":"NO ACCESS PLEASE LOGIN AGAIN"}

#     if request.method == 'GET':
#         try:
#             id = int(id)
#             emp_det = team_col.find_one({"emp_id": id})
#             emp_det = json.loads(json_util.dumps(emp_det))
#             return emp_det
#         except Exception as e:
#             return {"status": False, "msg": "Error Occured From Server Side", "error": str(e)}
#     return {"status":False,"msg":"method not allowed"}
# #----------------------------------------------------------------
# """
# These apis are used to manage testimonials
# """
# @app.route('/addtestimonial/',methods=['POST'])# add testimonial from index by customer himself
# def addtestimonial():
#     if request.method=='POST':
#         try:
#             test_data=json.loads(request.data)
#             if test_data['photo']!='':
#                 base64_data = re.sub('^data:image/.+;base64,', '', test_data [ 'photo' ])
#                 im = Image.open(io.BytesIO(base64.b64decode(base64_data)))
#                 im = im.resize((100,100))
#                 im = im.convert('RGB')
#                 curpath = os.getcwd()
#                 curpath += "/static/images/clients/tempimg.jpg"
#                 im.save(curpath, 'JPEG', quality=50)
#                 with open(curpath, 'rb') as f:
#                     content = f.read()
#                 file = fs.put(content, filename=''.join(random.choices(string.ascii_letters+string.digits, k=5))+'.jpg')
#                 os.remove(curpath)
#             else:
#                 file=''
#             if test_col.find_one(sort=[ ("tid", -1) ]) == None:
#                 tid = 1
#             else:
#                 tid = test_col.find_one(sort=[ ("tid", -1) ]) [ 'tid' ]+1
#             test_col.insert_one({
#                 "tid":tid,
#                 "name":test_data['name'],
#                 "img":str(file),
#                 "designation":test_data['desig'],
#                 "description":test_data['desc'],
#                 "updated_date":str(datetime.datetime.today()),
#                 "status":0
#             })
#             return {"status":True,"msg":"Your Feedback Recorded,Thank You."}
#         except Exception as e:
#             return {"status": False, "msg": "Error Occured From Server Side","error":str(e)}

#     return {"status":False,"msg":"Method Not Allowed"}
# @app.route("/testimonialaction/<tid>/<taction>/<token>",methods=['GET'])#verify the testimonial by admin
# def testimonialaction(tid,taction,token):
#     if token not in active_tokens:
#         return {"status":False,"cat":"logout","msg":"NO ACCESS PLEASE LOGIN AGAIN"}
#     try:
#         tid=int(tid)
#         status=test_col.find_one({"tid":tid})
#         if status['status']==1 or status['status']==2:
#             return {"status":False,"msg":"Action already recorded","tid":tid}
#         if taction=='accept':
#             test_col.update_one({"tid":tid},{"$set":{"status":1}})
#             return {"status":True,"cat":"accept","tid":tid}
#         elif taction=='reject':
#             test_col.update_one({"tid": tid}, {"$set": {"status": 2}})
#             return {"status":True,"cat":"reject","tid":tid}
#         else:
#             return {"status":False,"msg":"Error Occured Please try again","tid":tid}
#     except Exception as e:
#         return {"status":False,"msg":"Error occured from server side please contact tech team","tid":tid,"error":str(e)}
# @app.route('/healthcheck/')
# def healthcheck():
#     return {"status":True}

# #----------------------------------------------------------------
# """
# End of the program
# MOBASA TECH TEAM:

# FRONT-END DEVELOPERS = BALARAM REDDY,MOIN
# BACK-END DEVELOPER = SAMEER SHAIK


# """
if __name__ == "__main__":
    # deploy on local network 0.0.0.0:80 with debugging mode
    app.run(host='0.0.0.0', port=80, debug=True)
