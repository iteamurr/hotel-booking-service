import src.domain.services.booking as booking_services
import src.presentation.api.routes.v1.dependencies.common_depends as common_depends
import src.shared_kernel.building_blocks.infractructure.uow as common_uow


def get_booking_service() -> booking_services.BookingService:
    session_factory = common_depends.SessionManager().get_session_maker()
    uow = common_uow.SQLAlchemyUnitOfWork(session_factory=session_factory)
    return booking_services.BookingService(uow=uow)
