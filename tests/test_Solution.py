from numpy.testing import assert_, assert_equal
from pytest import raises as assert_raises

from pyjobshop.Model import Model
from pyjobshop.Solution import Solution, Task


def test_task_eq():
    """
    Tests the equality comparison of tasks.
    """
    task1 = Task(0, 1, 2, 3)

    assert_equal(task1, Task(0, 1, 2, 3))
    assert_(task1 != Task(0, 1, 2, 4))


def test_solution_eq(small):
    """
    Tests the equality comparison of solutions.
    """
    schedule = [Task(0, 0, 0, 1), Task(1, 0, 1, 2)]
    sol1 = Solution(small, schedule)

    assert_equal(sol1, Solution(small, schedule))
    other = [Task(0, 0, 0, 1), Task(0, 0, 3, 2)]
    assert_(sol1 != Solution(small, other))


def test_solution_raises_invalid_schedule():
    """
    Tests that a ``ValueError`` is raised when a solution is created with an
    invalid schedule. In this case, it only checks whether tasks are
    assigned to eligible machines.
    """
    model = Model()

    job = model.add_job()
    machines = [model.add_machine() for _ in range(2)]
    tasks = [model.add_task(job=job) for _ in range(2)]

    for duration, (task, machine) in enumerate(zip(tasks, machines), 1):
        model.add_processing_time(task, machine, duration)

    data = model.data()

    # Invalid schedule: task 0 is scheduled on machine 1.
    schedule = [Task(0, 1, 0, 1), Task(1, 1, 1, 2)]

    with assert_raises(ValueError):
        Solution(data, schedule)
