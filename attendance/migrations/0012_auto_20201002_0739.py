# Generated by Django 3.1 on 2020-10-02 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0011_auto_20201001_1651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject_faculty',
            name='faculty',
        ),
        migrations.RemoveField(
            model_name='subject_faculty',
            name='id',
        ),
        migrations.RemoveField(
            model_name='subject_faculty',
            name='subject',
        ),
        migrations.AddField(
            model_name='subject_faculty',
            name='faculty_shift_1',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='subject_faculty',
            name='faculty_shift_2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='subject_faculty',
            name='subject_code',
            field=models.CharField(choices=[('310901', '310901'), ('310902', '310902'), ('310903', '310903'), ('310904', '310904'), ('310905', '310905'), ('310906', '310906'), ('310907', '310907'), ('310908', '310908'), ('310909', '310909'), ('310910', '310910'), ('310911', '310911'), ('310912', '310912'), ('310913', '310913'), ('310914', '310914'), ('310915', '310915'), ('310916', '310916'), ('410901', '410901'), ('410902', '410902'), ('410903', '410903'), ('410904', '410904'), ('410905', '410905'), ('410906', '410906'), ('410907', '410907'), ('410908', '410908'), ('410909', '410909'), ('410910', '410910'), ('410911', '410911'), ('410912', '410912'), ('410913', '410913'), ('410914', '410914'), ('410915', '410915'), ('410916', '410916'), ('510901', '510901'), ('510902', '510902'), ('510903', '510903'), ('510904', '510904'), ('510905', '510905'), ('510906', '510906'), ('510907', '510907')], default='310901', max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='subject_faculty',
            name='subject_name',
            field=models.CharField(choices=[('C and C++ Programming', 'C and C++ Programming'), ('Computer Organization', 'Computer Organization'), ('Principles of Programming Practices', 'Principles of Programming Practices'), ('Discrete Mathematics', 'Discrete Mathematics'), ('Probability & Statistics', 'Probability & Statistics'), ('Business Communications', 'Business Communications'), ('C & C++ Laboratory', 'C & C++ Laboratory'), ('Open Source Tools Laboratory', 'Open Source Tools Laboratory'), ('Java Programming', 'Java Programming'), ('Data Structures using C', 'Data Structures using C'), ('Web Technologies', 'Web Technologies'), ('System Analysis & Design', 'System Analysis & Design'), ('Management Theory & Practices', 'Management Theory & Practices'), ('Web Technologies Laboratory', 'Web Technologies Laboratory'), ('Java Programming Laboratory', 'Java Programming Laboratory'), ('Data Structures Laboratory', 'Data Structures Laboratory'), ('Advanced Java', 'Advanced Java'), ('DBMS', 'DBMS'), ('Operating Systems', 'Operating Systems'), ('OOAD', 'OOAD'), ('Operations Research', 'Operations Research'), ('HBASE Lab', 'HBASE Lab'), ('Advance Java Lab', 'Advance Java Lab'), ('UML Lab – umbrello', 'UML Lab – umbrello'), ('Advanced Web Technology', 'Advanced Web Technology'), ('Banking and FAM', 'Banking and FAM'), ('CN & Information Security', 'CN & Information Security'), ('Elective I ', 'Elective I '), ('Adv DBMS', 'Adv DBMS'), ('WT Lab', 'WT Lab'), ('Advance DBMS Lab', 'Advance DBMS Lab'), ('Network & Security Lab', 'Network & Security Lab'), ('Recent Technologies in IT', 'Recent Technologies in IT'), ('Software Testing and Quality Assurance', 'Software Testing and Quality Assurance'), ('Software Engineering', 'Software Engineering'), ('Data warehousing, data mining and BI', 'Data warehousing, data mining and BI'), ('Elective - II', 'Elective - II'), ('RTIT Lab', 'RTIT Lab'), ('STQA Lab', 'STQA Lab')], max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
    ]
