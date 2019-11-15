from django.db.models import Count
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Job, Post


class UserJobListView(LoginRequiredMixin,ListView):
    """
    list the jobs for the current user
    """
    model = Job
    template_name = 'jobtracker/home.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        user = self.request.user
        return Job.objects.filter(creator=user).order_by('status','-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        Job.objects.annotate(population=Count('post'))

        # get the counts, and set in the returned context
        active_count = 0
        inactive_count = 0
        obsolete_count = 0
        userjobs = Job.objects.filter(creator=user)
        for j in userjobs:
            if j.status == 'Active':
                active_count += 1
            elif j.status == 'Inactive':
                inactive_count += 1
            else:
                obsolete_count += 1
        context['active_count'] = active_count
        context['inactive_count'] = inactive_count
        context['obsolete_count'] = obsolete_count
        return context


def about(request):
    """
    redirect to about page
    """
    return render(request, 'jobtracker/about.html', {'title': 'About Jobtracker'})


class JobDetailView(LoginRequiredMixin, DetailView):
    """
    display the job details
    """
    model = Job


class JobCreateView(LoginRequiredMixin, CreateView):
    """
    create a new job for the logged in user
    """
    model = Job
    fields = ['title', 'location', 'url', 'job_id', 'agency', 'agency_contact',
              'agency_contact_telnum', 'description', 'cv', 'cover_letter', 'status']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class JobPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    post an existing job for the logged in user
    """
    model = Job
    fields = ['title', 'location', 'url', 'job_id', 'agency', 'agency_contact',
              'agency_contact_telnum', 'description', 'cv', 'cover_letter', 'status']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        job = self.get_object()
        if self.request.user == job.creator:
            return True
        return False


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    delete an existing job for the logged in user
    """
    model = Job
    success_url = '/'

    def test_func(self):
        job = self.get_object()
        if self.request.user == job.creator:
            return True
        return False


class PostListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    display the posts for a selected job
    """
    model = Post
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        job = Job.objects.filter(id=pk).first()
        context['posts'] = Post.objects.filter(creator=job).order_by('-date_posted')
        context['parent_job'] = {'id': job.id,'title': job.title}
        return context

    def test_func(self):
        # check the job is associated with the parent Job (given by 'pk')
        job = Job.objects.filter(id=self.kwargs['pk']).first()
        if job is None:
            return False
        return True


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    create a new post for the selected job
    """
    model = Post
    fields = ['description', 'attachment']

    def get_success_url(self, **kwargs):
        if kwargs != None:
            pkasstr = str(self.kwargs['pk'])
            return reverse('post-list',args=(pkasstr,))
        else:
            # havent tested this path
            return reverse('post-list', args=(self.object.id,))

    def form_valid(self, form):
        pk = self.kwargs['pk']
        job = Job.objects.filter(id=pk).first()
        form.instance.creator = job
        return super().form_valid(form)

    def test_func(self):
        # check the job is associated with the parent Job (given by 'pk')
        job = Job.objects.filter(id=self.kwargs['pk']).first()
        if job is None:
            return False
        return True

class PostPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    edit an existing post:
    """
    model = Post
    fields = ['description', 'attachment']

    def get_success_url(self, **kwargs):
        if kwargs != None:
            jobidasstr = str(self.kwargs['jobid'])
            return reverse('post-list',args=(jobidasstr,))
        else:
            # havent tested this path
            return reverse('post-list', args=(self.object.id,))

    def test_func(self):
        # check its a valid job
        job = Job.objects.filter(id=self.kwargs['jobid']).first()
        if job is None:
            return False
        # check its a valid post
        job = self.get_object()
        post = Post.objects.filter(id=self.kwargs['pk']).first()
        if post is None:
            return False
        return True


class PostDetailView(LoginRequiredMixin, DetailView):
    """
    display the job details
    """
    model = Post


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    delete an existing job for the logged in user only
    """
    model = Post

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        post = Post.objects.filter(id=pk).first()
        context['parent_job'] = {'id': post.creator_id}
        return context

    def test_func(self):
        # check its a valid job
        job = Job.objects.filter(id=self.kwargs['jobid']).first()
        if job is None:
            return False
        # check its a valid post
        job = self.get_object()
        post = Post.objects.filter(id=self.kwargs['pk']).first()
        if post is None:
            return False
        return True

    def get_success_url(self, **kwargs):
        if kwargs != None:
            jobidasstr = str(self.kwargs['jobid'])
            return reverse('post-list',args=(jobidasstr,))
        else:
            # havent tested this path
            return reverse('post-list', args=(self.object.id,))
