from datetime import date

from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.repositories.sessao_repository import SessaoRepository
from app.utils.validators import BusinessError


class AvaliacaoService:
    def __init__(self):
        self.repo = AvaliacaoRepository()
        self.sessoes = SessaoRepository()

    def listar(self, usuario):
        if usuario.papel == "ESTUDANTE":
            return self.repo.list_by_estudante(usuario.id_usuario)
        if usuario.papel == "PROFESSOR":
            return self.repo.list_by_professor(usuario.id_usuario)
        return self.repo.list_all()

    def listar_recebidas(self, id_monitor):
        return self.repo.list_recebidas_monitor(id_monitor)

    def resumo_monitor(self, id_monitor):
        return self.repo.list_resumo_monitor(id_monitor)

    def listar_feitas(self, id_monitor):
        return self.repo.list_by_estudante(id_monitor)

    def criar(self, sessao_id, estudante, data):
        sessao = self.sessoes.get_by_id(sessao_id)
        if not sessao or not sessao.realizada:
            raise BusinessError("A avaliação só pode ser feita para sessão realizada.")
        if sessao.id_estudante != estudante.id_usuario:
            raise BusinessError("Você não pode avaliar uma sessão que não é sua.")
        if self.repo.find_by_sessao_estudante(sessao_id, estudante.id_usuario):
            raise BusinessError("Você já avaliou esta sessão.")
        return self.repo.create(
            {
                "id_sessao": int(sessao_id),
                "id_estudante": estudante.id_usuario,
                "nota": int(data["nota"]),
                "comentario": data.get("comentario", ""),
                "data_avaliacao": date.today().isoformat(),
            }
        )
