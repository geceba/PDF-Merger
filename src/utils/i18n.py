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
        'btn_merge': "Aplicar Cambios y Unir",
        'msg_no_pdfs': "No hay PDFs",
        'msg_success': "PDF listo",
        'title': "PDF Merger",
        'preview_title': "Vista Previa",
        'exclude_label': "Excluir",
        'success_title': "¡Listo!",
        'warning_title': "Aviso",
        'msg_conversion_success': "Archivo Word listo",
        'msg_conversion_error': "La conversión falló. El PDF podría ser un escaneo o basado en imagen.",
        'error_title': "Error"
    },
    'en': {
        'empty_msg': "Drag PDFs here or click 'Add'",
        'btn_add': "Add",
        'btn_clear': "Clear",
        'btn_up': "Up",
        'btn_down': "Down",
        'btn_merge': "Apply Changes & Merge",
        'msg_no_pdfs': "No PDFs found",
        'msg_success': "PDF ready",
        'title': "PDF Merger",
        'preview_title': "Preview",
        'exclude_label': "Exclude",
        'success_title': "Ready!",
        'warning_title': "Warning",
        'msg_conversion_success': "Word file ready",
        'msg_conversion_error': "Conversion failed. The PDF might be scanned or image-based.",
        'error_title': "Error"
    }
}

LANG = get_system_lang()
TEXTS = STRINGS[LANG]