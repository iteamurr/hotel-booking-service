import src.domain.services.booking as booking_services
import src.domain.services.hotel as hotel_services
import src.infrastructure.db.repositories.uow as uow_repos
import src.presentation.api.dependencies.session as api_depends


def get_booking_service() -> booking_services.BookingService:
    session_factory = api_depends.SessionManager().get_session_maker()
    uow = uow_repos.SQLAlchemyUnitOfWork(session_factory=session_factory)
    return booking_services.BookingService(uow=uow)


def get_hotel_service() -> hotel_services.HotelService:
    session_factory = api_depends.SessionManager().get_session_maker()
    uow = uow_repos.SQLAlchemyUnitOfWork(session_factory=session_factory)
    return hotel_services.HotelService(uow=uow)
