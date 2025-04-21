import src.domain.services.hotel as hotel_services
import src.presentation.api.routes.v1.dependencies.common_depends as common_depends
import src.shared_kernel.building_blocks.infractructure.uow as common_uow


def get_hotel_service() -> hotel_services.HotelService:
    session_factory = common_depends.SessionManager().get_session_maker()
    uow = common_uow.SQLAlchemyUnitOfWork(session_factory=session_factory)
    return hotel_services.HotelService(uow=uow)
