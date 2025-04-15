import src.api.dependencies.session as api_depends
import src.api.services.booking as booking_services
import src.api.services.hotel as hotel_services
import src.database.crud.uow as crud_uow


def get_booking_service() -> booking_services.BookingService:
    session_factory = api_depends.SessionManager().get_session_maker()
    uow = crud_uow.SQLAlchemyUnitOfWork(session_factory=session_factory)
    return booking_services.BookingService(uow=uow)


def get_hotel_service() -> hotel_services.HotelService:
    session_factory = api_depends.SessionManager().get_session_maker()
    uow = crud_uow.SQLAlchemyUnitOfWork(session_factory=session_factory)
    return hotel_services.HotelService(uow=uow)
