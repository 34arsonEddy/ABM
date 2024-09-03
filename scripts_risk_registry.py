import os
import random
import django
from django.conf import settings
from django.test.utils import get_runner
from decimal import Decimal




os.environ["DJANGO_SETTINGS_MODULE"] = "riskregistry.settings"
django.setup()
from api.factory import UserFactory
from api.models.risk import Risk_IA
from api.models.abbreviation import AffectedArea, Category, Process, RiskType
from api.models.role import Role
from api.models.stackholder import Stackholder
from api.models.user import User
from services.risk_IA import Risk_IAService



if __name__ == "__main__":
    print("init")
    
    # print(f'{settings.LDAP_BIND_DN}\\ teste')
    # # create user
    # Stackholder.objects.create(title="teste", name="teste")
    # stackholder = Stackholder.objects.get(id=1)
    # role = Role.objects.create(title="teste", name="teste")
    # role = Role.objects.get(id=1)
    # User.objects.create_user(session="admin", password="admin", email="admin@gmail.com", stackholder=stackholder, role=role)
    
    # create a role 
    # print(User.objects.filter(None))
    
    
    # process = Process.objects.create(name = "process")
    
    
    # creation risk ia
    # risk_ia = Risk_IA.objects.create(
    #     reference = "2.1",
    #     process_objectives = "teste",
    #     inherent_risk_description = "inherent_risk_description",
    #     probability = 1,
    #     impact = 1,
    #     nature_of_control = "nature_of_control",
    #     automatic_or_manual_control = "automatic_or_manual_control",
    #     quality_of_the_control = "quality_of_the_control",
    #     residual_risk_level = "residual_risk_level",
    #     detail_of_strategy = "detail_of_strategy",
    # )
    
    from django.db.models import Q
    # r= Risk_IA.objects.filter(Q(date_of_assessment__range=["23-12-2024", "24-12-2024"]))
    # print(r)
    
    
    from api.models.abbreviation import Subprocess
    from api.models.abbreviation import Process
    
    # p = Process.objects.create(id=2, name="process2", description="")
    # subprocess = Subprocess.objects.create(id=2, name="subprocess2", process=p)
    
    from django.db import connection


    # users = User.objects.all().delete()
    # users = Subprocess.objects.all().delete()
    # users = Process.objects.all().delete()
    
    # Creation fake_user
    # UserFactory.create_batch(50)
    
    # users = User.objects.all()
    # for user in users:
    #     user.set_password('hello')
    #     user.save()
    
    #creer le process et subprocess
    # processCMicro = Process.objects.create(name="Crédit Micro")
    # processCPME = Process.objects.create(name="Crédit PME")
    # processCAgro = Process.objects.create(name="Crédit Agro")
    # processCparticulier = Process.objects.create(name="Crédit au particulier")
    
    # subprocess1 = Subprocess.objects.create(name="Acquisition des clients", process=processCMicro)
    # subprocess2 = Subprocess.objects.create(name="Analyse et enregistrement", process=processCMicro)
    # subprocess3 = Subprocess.objects.create(name="Formalisation et décaissement", process=processCMicro)
        
    # subprocess1 = Subprocess.objects.create(name="Acquisition des clients", process=processCPME)
    # subprocess2 = Subprocess.objects.create(name="Analyse et enregistrement", process=processCPME)
    # subprocess3 = Subprocess.objects.create(name="Formalisation et décaissement", process=processCPME)
    
    
    # risk_type = RiskType(id=5, name="Fraud", description="teste")
    # risk_type.save(update_fields=['name', 'description'])
    
    
    
    #insertion de risk_ia factory
    
    from django.db import connection



    def truncate_app_model(table):
        sql_truncate = f"TRUNCATE TABLE api_{table};"
        sql_reset_identity = f"DBCC CHECKIDENT ('api_{table}', RESEED, 0);"
        with connection.cursor() as cursor:
            cursor.execute(sql_truncate)
            cursor.execute(sql_reset_identity)
            
    truncate_app_model('risk_ia_affected_area')
    truncate_app_model('risk_ia_category')
    truncate_app_model('risk_ia_risk_type')
    
    i = 1
    processInit = Subprocess.objects.all()[0].process
    Risk_IA.objects.all().delete() # vider la table risk_ia
    for subprocess in Subprocess.objects.all():
        print(processInit.name)
        print(subprocess.process.name)
        print(i)
        # Prendre le numero de reference
        if subprocess.process == processInit:
            i += 1
        
        else:
            processInit == subprocess.process
            i = 1
        
        stackholder = Stackholder.objects.get(id=random.choices(range(1, Stackholder.objects.count()))[0])
        initiator = User.objects.filter(role__title=Role.RESPONSABLE_RISK_ASSESSMENT).first()
        riskType = RiskType.objects.get(id=random.choices(range(1, RiskType.objects.count()))[0])
        affected_area = AffectedArea.objects.filter(id=random.choices(range(1, AffectedArea.objects.count()))[0]).first()
        category = Category.objects.filter(id=random.choices(range(1, Category.objects.count()))[0]).first()
        inherent_risk_level=Risk_IAService.get_inherent_risk_level(random.choices(range(1,10))[0])
        quality_of_the_control=random.choices(['Strong', 'Acceptable', 'Weak'])[0]
        residual_risk_level = Risk_IAService.get_residual_risk_level(inherent_risk_level=inherent_risk_level, quality_of_the_control=quality_of_the_control)
        risk = Risk_IA.objects.create(
            reference=f"{subprocess.process.id}.{i}",
            subprocess=subprocess,
            process_objectives="example",
            inherent_risk_description="example",
            probability=random.choices([1, 2, 3])[0],
            impact=random.choices([1, 2, 3])[0],
            inherent_risk_level=inherent_risk_level,
            controls_in_place="example",
            nature_of_control=random.choices(['Preventive', 'Detective', 'Directive', 'Compensating'])[0],
            automatic_or_manual_control=random.choices(['Manual','Automatic','Semi automatic'])[0],
            quality_of_the_control=quality_of_the_control,
            residual_risk_level=residual_risk_level,
            risk_strategy=random.choices(['Tolerate', 'Treat', 'Transfert', 'Terminate'])[0],
            detail_of_strategy="example",
            initiator=initiator
        )
        
        risk.stackholder.add(stackholder)
        risk.risk_type.add(riskType)
        risk.affected_area.add(affected_area)
        risk.category.add(category)
