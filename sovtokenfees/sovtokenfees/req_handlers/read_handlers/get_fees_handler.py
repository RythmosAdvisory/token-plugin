from sovtokenfees import FeesTransactions
from sovtokenfees.constants import FEES
from sovtokenfees.req_handlers.fees_utils import get_fee_from_state

from plenum.common.constants import STATE_PROOF, CONFIG_LEDGER_ID, BLS_LABEL
from plenum.common.request import Request
from plenum.common.types import f
from plenum.server.database_manager import DatabaseManager
from plenum.server.request_handlers.handler_interfaces.read_request_handler import ReadRequestHandler


class GetFeesHandler(ReadRequestHandler):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager, FeesTransactions.GET_FEES.value, CONFIG_LEDGER_ID)

    def get_result(self, request: Request):
        fees, proof = get_fee_from_state(self.state, is_committed=True, with_proof=True,
                                         bls_store=self.database_manager.get_store(BLS_LABEL))
        result = {f.IDENTIFIER.nm: request.identifier,
                  f.REQ_ID.nm: request.reqId,
                  FEES: fees}
        if proof:
            result[STATE_PROOF] = proof
        result.update(request.operation)
        return result