from datetime import datetime

AUDIT_LOG = []


def registrar_auditoria(usuario_id, acao, entidade, detalhes):
    registro = {
        "quando": datetime.now().isoformat(timespec="seconds"),
        "usuario_id": usuario_id,
        "acao": acao,
        "entidade": entidade,
        "detalhes": detalhes,
    }
    AUDIT_LOG.append(registro)
    print(f"[AUDITORIA] {registro}")
    return registro
