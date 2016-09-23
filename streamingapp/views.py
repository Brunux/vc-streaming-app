import django.views.generic
from django.views.generic.edit import FormView
from .forms import StreamingForm
from .models import Streaming
from django.shortcuts import redirect
import datetime, uuid

class Home(django.views.generic.TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        # Streamings filter by today
        streamings = Streaming.objects.filter(init_date=datetime.date.today())
        
        if len(streamings) == 1:
            if len(streamings[0].title) > 50:
                    streamings[0].title = streamings[0].title[:50] + " ..."
            context['streaming'] = streamings[0]
        
        elif len(streamings) > 1:
            for streaming in streamings:
                if len(streaming.title) > 50:
                    streaming.title = streaming.title[:50] + " ..."
            context['streamings'] = streamings
        
        return context
home = Home.as_view()

class StreamingCreateView(FormView):
    template_name = "create-streaming.html"
    form_class = StreamingForm
    success_url = '/done-create-streaming/'
    
    duration = False

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # Check StreamingForm to set manually user_email and uuid fields.
        if form.cleaned_data['duration'] == '1':
            duration = datetime.time(1,0)
        elif form.cleaned_data['duration'] == '30':
            duration = datetime.time(0,30)
        elif form.cleaned_data['duration'] == '15':
            duration = datetime.time(0,15)
        else:
            duration = False
        
        if duration:        
            streaming = Streaming(
                    user = 'brunux@virtuososcode.com',
                    title = form.cleaned_data['title'],
                    init_date = form.cleaned_data['init_date'],
                    init_time = form.cleaned_data['init_time'],
                    duration = duration,
                    uuid = uuid.uuid4(),
                    info = form.cleaned_data['info'],
                    is_public = form.cleaned_data['is_public']
                )
            streaming.save()
            
            self.request.session['uuid'] = str(streaming.uuid)
            self.request.session['title'] = str(streaming.title)
            self.request.session['init_date'] = str(streaming.init_date)
            self.request.session['init_time'] = str(streaming.init_time)
            self.request.session['user'] = str(streaming.user)
            
            return super(StreamingCreateView, self).form_valid(form)
        return redirect(error_view)
        
    def get_context_data(self, **kwargs):
        context = super(StreamingCreateView, self).get_context_data(**kwargs)
        # Need to get streaming object by URL to pass to the template tags,
        # check URL dispatcher docs.
        return context
streaming_create_view = StreamingCreateView.as_view()

# This should be used with the home form to access a streaming with a given uuid.
class StreamingView(django.views.generic.TemplateView):
    template_name = "streaming.html"
streaming_view = StreamingView.as_view()

# This should be used with the home streamings links avalables to access the
# selected streaming.
class StreamingViewLinked(django.views.generic.TemplateView):
    template_name = "streaming.html"
    
    def get_context_data(self, **kwargs):
        context = super(StreamingViewLinked, self).get_context_data(**kwargs)
        # Need to get streaming object by URL to pass to the template tags,
        # check URL dispatcher docs.
        context['streaming'] = Streaming.objects.get(uuid=self.request.path.replace("/",""))
        return context
streaming_view_linked = StreamingViewLinked.as_view()

# This should be used to render a successful streaming added
class DoneCreateStreamingView(django.views.generic.TemplateView):
    template_name = "done-create-streaming.html"
    context_object_name = 'streaming'
done_create_streaming_view = DoneCreateStreamingView.as_view()

# This should be used to display all posible errors
class ErrorView(django.views.generic.TemplateView):
    template_name = "error.html"
error_view = ErrorView.as_view()