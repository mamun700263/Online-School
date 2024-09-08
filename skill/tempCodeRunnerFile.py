class CourseModel(models.Model):
    name = models.CharField(max_length=120)
    taken_by = models.ForeignKey(TeacherAccount, on_delete=models.CASCADE, related_name='account',null = True)
    description = models.TextField(default="description")  
    skills = models.ManyToManyField(SkillModel)  
    thumbnail = models.URLField(null=True, blank=True)
    paid = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    time = models.IntegerField(help_text="Time in hours")
    rating = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.name} taken by {self.taken_by.user.first_name} {self.taken_by.user.last_name}"
