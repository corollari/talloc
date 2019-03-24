from simanneal import Annealer
import random

def rand(vec):
    return random.randint(0, len(vec) - 1)


# Constant data (DO NOT CHANGE WHILE THE ANNEALER IS RUNNING)

# TODO: Add time preferences in professor data and take them into account in the cost function
professors=[
    {
    'department': 2, # department id
    'preferences': {2:0.8, 0:0.2}, # courseIds order by preference
    'worklength': 20*60 # Minutes each professor should work
    },
    {
    'department': 2, # department id
    'preferences': {1:0.6, 0:0.4}, # courseIds order by preference
    'worklength': 20*60 # Minutes each professor should work
    },
    {
    'department': 2, # department id
    'preferences': {3:0.1, 2:0.9}, # courseIds order by preference
    'worklength': 20*60 # Minutes each professor should work
    }
]

courses=[
    {
    'faculty': 0, #faculty id
    'coreDegree': False,
    'onlySpecificDepartment': None, # None if it's not required or the department id if it's required
    'sessions': [ # Data on all the sessions that are part of a course
        { # Note: session length is implicit as start and end times are given
            'day': 0, # 0 - monday, 4 - friday
            'start': 9*60, # in minutes since the beginning of the day (12 am)
            'end': 10*60 # in minutes since the beginning of the day (12 am)
        },
        {
            'day': 4,
            'start': 13*60,
            'end': 14*00
        }]
    },
    {
    'faculty': 1, #faculty id
    'coreDegree': False,
    'onlySpecificDepartment': None, # None if it's not required or the department id if it's required
    'sessions': [ # Data on all the sessions that are part of a course
        { # Note: session length is implicit as start and end times are given
            'day': 0, # 0 - monday, 4 - friday
            'start': 12*60, # in minutes since the beginning of the day (12 am)
            'end': 14*60 # in minutes since the beginning of the day (12 am)
        },
        {
            'day': 1,
            'start': 9*60,
            'end': 11*60
        },
        {
            'day': 2,
            'start': 10*60,
            'end': 12*60
        }]
    },
    {
    'faculty': 2, #faculty id
    'coreDegree': False,
    'onlySpecificDepartment': None, # None if it's not required or the department id if it's required
    'sessions': [ # Data on all the sessions that are part of a course
        { # Note: session length is implicit as start and end times are given
            'day': 1, # 0 - monday, 4 - friday
            'start':12*60, # in minutes since the beginning of the day (12 am)
            'end': 13*60 # in minutes since the beginning of the day (12 am)
        },
        {
            'day': 2,
            'start': 9*60,
            'end': 11*60
        }]
    },
    {
    'faculty': 3, #faculty id
    'coreDegree': False,
    'onlySpecificDepartment': None, # None if it's not required or the department id if it's required
    'sessions': [ # Data on all the sessions that are part of a course
        { # Note: session length is implicit as start and end times are given
            'day': 1, # 0 - monday, 4 - friday
            'start': 10*60, # in minutes since the beginning of the day (12 am)
            'end': 13*60 # in minutes since the beginning of the day (12 am)
        },
        {
            'day': 3,
            'start': 12*60,
            'end': 14*60
        },
        {
            'day': 4,
            'start': 9*60,
            'end': 11*60
        }]
    }
]

def sessionOverlap(s1, s2): #TODO
    return sess1['day']==sess2['day']

def facultyDifference(s1, s2): #TODO
    return sess1['day']==sess2['day']

CONSTRAINED=float("inf")
MAX_MINUTES_PER_DAY=500

class Optimizer(Annealer):
    def move(self):
        """Assigns a random course to a random professor."""
        courseId = rand(courses)
        professorId = rand(professors)
        self.state[courseId] = professorId
    def energy(self):
        """Evaluates the cost function on the current state."""
        # TODO: Implement consecutive year constraints
        e = 0
        for profId, prof in enumerate(professors):
            profCourses=[cour for courId, cour in enumerate(courses) if self.state[courId]==profId]
            profCourseIds=[courId for courId, cour in enumerate(courses) if self.state[courId]==profId]
            profSessions=[]
            for cour1 in profCourses:
                for cour2 in profCourses:
                    if(cour1==cour2):
                        continue
                    for sess1 in cour1['sessions']:
                        for sess2 in cour2['sessions']:
                            if sessionOverlap(sess1, sess2):
                                return CONSTRAINED
                            if facultyDifference(sess1, sess2):
                                return CONSTRAINED
                if cour1['onlySpecificDepartment']!=None and cour1['onlySpecificDepartment']!=prof['department']:
                    return CONSTRAINED
                profSessions+=cour1['sessions']
            # calculate num hours
            e += (sum([s['end']-s['start'] for s in profSessions]) - prof['worklength'])**2
            # calculate num subjects
            e += len(profCourses)**2
            # calculate preferences matching
            # calculate temporal proximity of sessions
            # punish if too many hours in any given day
            for d in range(5):
                dayHours=sum([s['end']-s['start'] for s in profSessions if s['day']==d])
                if dayHours>MAX_MINUTES_PER_DAY:
                    e+=(MAX_MINUTES_PER_DAY-dayHours)**2
        return e

initial_state = [rand(professors) for x in range(len(courses))]
assignations, cost = Optimizer(initial_state).anneal()
