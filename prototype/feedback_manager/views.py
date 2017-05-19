from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.core import serializers

from models import *
from datetime import datetime
import pdb

class FeedBackView(View):
	"""
	"""

	def get(self, request, code):
		"""
		"""
		obj = Feedback.objects.get(code=code)
		user = obj.user
		grade_obj = UserGradeMap.objects.filter(user=user)
		if not obj.is_completed():
			obj.start_feedback()
			if obj.feedback_type.is_results():
				obj.end_feedback()
			return render(request, 'feedback_form.html', {'objs':obj, 'grade_objs':grade_obj})
		else:
			return render(request, 'thanks.html', {'msg': 'Oops! You have already submitted this feedback'})

	def post(self, request, code):
		"""
		"""
		print "request  >> ", request.POST
		feedback_obj = Feedback.objects.get(code=code)
		feedback_qusetion_map_ids = request.POST.getlist('feedback_qusetion_map_id')
		for index, feedback_qusetion_map_id in enumerate(feedback_qusetion_map_ids):
			obj = FeedbackQusetionMap.objects.get(id=feedback_qusetion_map_id)
			if obj.question.is_subjective():
				answer = request.POST.get("answer-%s" %(feedback_qusetion_map_id))
				obj.submitted_answer = answer
				obj.submitted_at=datetime.now()
				obj.save()
			elif obj.question.is_objective():
				answer = request.POST.get("answer-%s" %(feedback_qusetion_map_id))
				option= Option.objects.get(id=answer)
				FeedbackQusetionOptionMap(feedback_qusetion_map=obj,
										  submitted_option=option).save()
				obj.submitted_at=datetime.now()
				obj.save()
			elif obj.question.is_appointment():
				appointment_id = request.POST.get('Time','')
				print "appointment_id  >>>>>>", appointment_id
				appointment_obj = NewAppointment.objects.get(id=appointment_id)
				appointment_obj.make_appointment()
				FeedbackAppointmentMap(feedback=feedback_obj, appointment=appointment_obj,
					submitted_at=datetime.now()).save()
			else:
				answer = request.POST.getlist("answer-%s" %(feedback_qusetion_map_id))
				for single_answer in answer:
					option= Option.objects.get(id=single_answer)
					FeedbackQusetionOptionMap(feedback_qusetion_map=obj,
												  submitted_option=option).save()
					obj.submitted_at=datetime.now()
					obj.save()
					
		obj = Feedback.objects.get(code=code)
		obj.end_feedback()
		return HttpResponseRedirect(reverse('view_thanks'))

class FeedbackSubmittedView(View):
	"""
	"""

	def get(self, request):
		"""
		"""
		return render(request, 'thanks.html', {'msg': 'Thanks for spending your valuable time with us. We have recorded your feedback.'})

class ViewFeedback(View):
	"""
	"""

	def get(self, request, feedback_id):
		feedback = Feedback.objects.get(id=feedback_id)
		if feedback.feedback_type.is_results():
			user_grade_map_obj = UserGradeMap.objects.filter(user=feedback.user)
			return render(request, 'view_feedback.html', {'feedback': feedback, 'user_grade_map_obj':user_grade_map_obj})
		elif feedback.feedback_type.is_appointment():
			feedback_appointment_obj = FeedbackAppointmentMap.objects.get(feedback=feedback)
			return render(request, 'view_feedback.html', {'feedback': feedback, 'feedback_appointment_obj':feedback_appointment_obj})
		else:
			return render(request, 'view_feedback.html', {'feedback': feedback})

class Home(View):
	def get(self, request):
		return render(request, 'calender.html')
	def post(self, request):
		date = request.POST.get('date','')
		dt = datetime.strptime(date, "%Y-%m-%d")
		weekday = dt.weekday()
		available_appointments = Appointment.objects.filter(day=weekday)
		return render(request, 'calender.html',{'data':date, 'available_appointments':available_appointments})

def avail_time_old(request):
	response_data = {}
	date = request.POST.get('date','')
	weekday = date
	available_appointments = Appointment.objects.filter(day=weekday, available='A')
	list1= []
	for obj in available_appointments:
		list1.append({'id':obj.id,'time':obj.start_time})
	#response_data['success'] = True
	#response_data['data'] = serializers.serialize('json', available_appointments)
	response = {'success':True, 'data': date, 'available_appointments': list1}
	#response = {'success':True, 'available_appointments': available_appointments}
	#return HttpResponse(JsonResponse(response_data), content_type="application/json")
	return JsonResponse(response)

def avail_time(request):
	response_data = {}
	date = request.POST.get('date','')
	date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
	print "date >>>>>>>>>>>>..", date
	available_appointments = NewAppointment.objects.filter(date=date, available='A')
	print "available_appointments  >>>>>>>>>>", available_appointments
	list1= []
	for obj in available_appointments:
		list1.append({'id':obj.id,'time':str(obj.time_slot)})
	#response_data['success'] = True
	#response_data['data'] = serializers.serialize('json', available_appointments)
	response = {'success':True, 'data': date, 'available_appointments': list1}
	#response = {'success':True, 'available_appointments': available_appointments}
	#return HttpResponse(JsonResponse(response_data), content_type="application/json")
	return JsonResponse(response)
