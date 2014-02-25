from django.shortcuts import render, redirect
from electoral_data.models import LokSabhaSeat,AssemblyConstituency,PollingStation,Citizen,CitizenInterestForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect

# Create your views here.
@login_required()
def index(request):
	if request.user.is_staff:
		return redirect(reverse('admin:index'))
	else:		
		return redirect(reverse('electoral_data.views.societies',args=[str(request.user.get_profile().polling_station.id)]))

# Show LS seats
@login_required()
def ls(request):
	if request.user.is_staff:
		ls_seats_list = LokSabhaSeat.objects.all()
		context = {'ls_seats_list': ls_seats_list}
		return render(request, 'electoral_data/ls.html', context)
	else:
		return redirect(reverse('electoral_data.views.societies',args=[str(request.user.get_profile().polling_station.id)]))
	
# Show Assembly seats for LS
@login_required()
def assembly(request,ls_id):
	if request.user.is_staff:
		assembly_list = AssemblyConstituency.objects.filter(lok_sabha_seat=ls_id)
		context = {'assembly_list': assembly_list}
		return render(request, 'electoral_data/assembly.html', context)
	else:
		return redirect(reverse('electoral_data.views.societies',args=[str(request.user.get_profile().polling_station.id)]))

# Show Polling booths for the Assembly seat
@login_required()
def polling(request,assembly_id):
	if request.user.is_staff:
		polling_list = PollingStation.objects.filter(constituency=assembly_id)
		context = {'polling_list': polling_list}
		return render(request, 'electoral_data/polling.html', context)
	else:
		return redirect(reverse('electoral_data.views.societies',args=[str(request.user.get_profile().polling_station.id)]))

# Show Citizens in the Society
@login_required()
def citizens(request,polling_station_id):
	citizens_list = Citizen.objects.filter(polling_station=polling_station_id)
	context = {'citizens_list': citizens_list,'polling_station':polling_station_id}
	return render(request, 'electoral_data/citizen.html', context)


# Show Citizen details
@login_required()
@csrf_protect
def detail(request,citizen_id):
	citizen_details = Citizen.objects.filter(id=citizen_id)
	if request.method == 'POST':
		form = CitizenInterestForm(request.POST, instance=citizen_details[0])
		form.save()
		polling_station_id = citizen_details[0].polling_station.polling_station_id
		return redirect(reverse('electoral_data.views.citizens',args=[polling_station_id]))
	else:
		form = CitizenInterestForm(instance=citizen_details[0])
		context = {'citizen_details': citizen_details,'form': form}
		return render(request, 'electoral_data/detail.html', context)
		
	
