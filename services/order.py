from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order(user=user)

    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(order_id=order.pk).update(
            created_at=order.created_at
        )


    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    qs = Order.objects.all()
    if username:
        qs = qs.filter(user__username=username)
    return qs
