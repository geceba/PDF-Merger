import locale

def get_system_lang():
    lang, _ = locale.getdefaultlocale()
    if lang and lang.startswith('es'):
        return 'es'
    return 'en'

STRINGS = {
    'es': {
        'empty_msg': "Arrastra PDFs aquí o haz clic en 'Agregar'",
        'btn_add': "Agregar",
        'btn_clear': "Limpiar",
        'btn_up': "Subir",
        'btn_down': "Bajar",
        'btn_merge': "Unir PDFs",
        'msg_no_pdfs': "No hay PDFs",
        'msg_success': "🔥 PDF listo",
        'title': "PDF Merger"
    },
    'en': {
        'empty_msg': "Drag PDFs here or click 'Add'",
        'btn_add': "Add",
        'btn_clear': "Clear",
        'btn_up': "Up",
        'btn_down': "Down",
        'btn_merge': "Merge PDFs",
        'msg_no_pdfs': "No PDFs found",
        'msg_success': "🔥 PDF ready",
        'title': "PDF Merger"
    }
}

LANG = get_system_lang()
TEXTS = STRINGS[LANG]