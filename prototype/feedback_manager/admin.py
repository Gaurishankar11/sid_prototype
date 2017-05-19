import random, string, datetime

from django.contrib import admin
from django.template import Context
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.contrib.admin import AdminSite
from django.core.mail import send_mail
from django.template.loader import render_to_string
from feedback_manager.models import *
from datetime import datetime, timedelta, date

def get_random_string(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def assign_feedback(modeladmin, request, queryset):
	feedback_types = FeedbackType.objects.all()
	for obj in queryset:
		for feedback_type in feedback_types:
			feedback_obj = Feedback(name=get_random_string(10),
									feedback_type=feedback_type,
									user=obj,
									created_by=request.user,
									code=get_random_string(16))
			feedback_obj.save()

			for question in feedback_type.questions.all():
				feedback_qusetion_map_obj = FeedbackQusetionMap(feedback=feedback_obj,
																question=question)
				feedback_qusetion_map_obj.save()
	send_mails(queryset)

assign_feedback.short_description = "Send feedback mail to selected users"

def send_mails(queryset):
	for user_obj in queryset:
		feedbacks = Feedback.objects.filter(user=user_obj, status='A')
		msg_html = render_to_string('email_temp.html', {'feedbacks': feedbacks, 'name':user_obj.username})

		subject='Feedback Mail'
		text_content = 'imp_mail'
		send_mail(subject, text_content, 'gaurishankar.neo@gmail.com',
				  [user_obj.email], html_message=msg_html)

class user_asign_feedback(admin.ModelAdmin):
    list_display = ['username']
    ordering = ['username']
    actions = [assign_feedback]


class OptionInline(admin.TabularInline):
    model = Option

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        OptionInline,
    ]

class FeedbackAdmin(admin.ModelAdmin):
	model=Feedback
	list_display = ('user', 'feedback_type', 'status', 'view')
	list_display_links = None
	actions = None
	def view(self, obj):
		return '<a href="%s">View</a>' % (reverse('view_feedback', kwargs={'feedback_id': obj.id}))

	view.allow_tags = True
	view.short_description = 'View Feedback'


class MyAdminSite(AdminSite):
    index_title = 'Monty Python administration'


def create_appointments(modeladmin, request, queryset):
	start_date = TimeTable.objects.all()[0].start_date
	end_date = TimeTable.objects.all()[0].end_date
	# start_time = TimeTable.start_time
	# end_time =  TimeTable.end_time
	print "queryset  ", dir(queryset)
	for obj in queryset:
		print "obj >>>>>", obj
		start_date = obj.start_date
		end_date = obj.end_date
		print "start_date  ", start_date
		print "end_date  ", end_date
		appointments = []
		#hours = (start_time, end_time)
		hours = (datetime(2012, 5, 22, 9), datetime(2012, 5, 22, 17,30))
		slots = get_slots(hours, appointments)
		for slot in slots:
			TimeSlot(appointment_time=slot, time_table=obj).save()
		date_range = daterange(start_date, end_date)
		for date in date_range:
			for slot in TimeSlot.objects.all():
				NewAppointment(date = date, time_slot=slot).save()

assign_feedback.short_description = "Send feedback mail to selected users"

def get_slots(hours, appointments, duration=timedelta(hours=1)):
    list1 = []
    slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])
    for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
	assert start <= end, "Cannot attend all appointments"
	while start + duration <= end:
	    list1.append("{:%H:%M} - {:%H:%M}".format(start, start + duration))
	    start += duration
	return list1

class create_apoointment(admin.ModelAdmin):
    list_display = ('start_date', 'end_date')
    ordering = ['start_date']
    actions = [create_appointments]

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


admin_site = MyAdminSite(name='myadmin')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Feedback, FeedbackAdmin)

admin.site.register(FeedbackType)
admin.site.unregister(User)
admin.site.register(User, user_asign_feedback)
admin.site.register([Subject, Grade, UserGradeMap, Day, FeedbackAppointmentMap])

admin.site.register(TimeTable,create_apoointment)