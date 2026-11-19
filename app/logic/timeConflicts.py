from app.models.models import Course, BannerSchedule, CrossListed


def slots_overlap(days_a, start_a, end_a, days_b, start_b, end_b):
    """
    True if a person couldn't attend both time slots: they share a day
    and their times overlap. Touching times (10:30 end / 10:30 start) don't count.
    """
    if not set(days_a) & set(days_b):
        return False
    return start_a < end_b and start_b < end_a


def get_time_conflict_groups(term_id):
    """
    Returns one group per time slot in the term. Each group has the slot and every
    course in that slot or in a slot that overlaps it. Only groups with 2+ courses.
    """
    courses = (Course.select(Course, BannerSchedule)
                     .join(BannerSchedule)
                     .where(Course.term == term_id,
                            Course.offCampusFlag == False,
                            BannerSchedule.sid != "ZZZ",
                            BannerSchedule.startTime.is_null(False),
                            BannerSchedule.endTime.is_null(False)))

    # Show each cross-listed course once: skip the copies
    copies = {row.crosslistedCourse_id for row in
              CrossListed.select().where(CrossListed.term == term_id,
                                         CrossListed.crosslistedCourse != CrossListed.courseId)}
    courses = [c for c in courses if c.cId not in copies]

    # Group courses by their time slot
    courses_by_slot = {}
    for course in courses:
        courses_by_slot.setdefault(course.schedule.sid, []).append(course)

    slots = {sid: group[0].schedule for sid, group in courses_by_slot.items()}
    slot_days = {sid: {d.day for d in slot.days} for sid, slot in slots.items()}

    groups = []
    for sid, slot in slots.items():
        members = []
        for other_sid, other in slots.items():
            if slots_overlap(slot_days[sid], slot.startTime, slot.endTime,
                             slot_days[other_sid], other.startTime, other.endTime):
                members.extend(courses_by_slot[other_sid])
        if len(members) >= 2:
            groups.append({"slot": slot, "courses": members})

    groups.sort(key=lambda g: g["slot"].order)
    return groups
