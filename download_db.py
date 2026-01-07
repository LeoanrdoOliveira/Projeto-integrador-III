import dropbox

# Configurações
ACCESS_TOKEN = 'sl.u.AF4CEX79ryZnIJFnMftSlRG1xfi1V7ABtLUg7RnjseCg3XT-3J2aTw6QD9CQEZOwiUrOTuTCo_SoyUrl-1AtyNbZZ722jPfRW28cq-x7Itt2X8uPovqSZUD8IEm2__PQp8mcI9uSpcU-F9Zep7beBXU3ekydxBp7kXQVVHjSo66HWz0y0S7b0_rhvwBluXKqtgp5uFI5Wi8gpQC4yAsLCmig42OPcQROTWzPkYwKILic5lU4kioclxFmyPqQVL_4iudOrQbwZC8EYCmorLyKktTsgfguLYcpTxVqKEVepEJidTQuEUWx8RMfy4XPOLawWMAnUit6sZya9-4mxr8hevOalJXjQrOoOR3WfAyWCaAYlU9l28vw9sG2WLxvwRLQDoTH2mt6u139ttdOkGx2y71C9G6ozRoBHktpwfMoRgylGbUZmH2-unqqFuJDym594TXL_OE0p9VMv0P752J940GSioXorZeXlEYYlNFgq-q2uLKa1SCN2e2eF1rUF8F-NLvXllMZzjWwciKS6r7aZt3c4VYaFoyAlEORxlCbL9M1hwYdajJ1Or3c7Jq1o5fV97GgESK3VXq7lVYSR_xFARNXGjkOHilWe04S7QVdbagoo_K71xUh6CoKs2bqxKiE4cpQQFHnhxHnUQDru0luXCCbnjf1IjCc8X0G3-KUQlh2winYKaGOCCdtEZ1wga2EZIEWzOmxncNul8JfVtANRMHO-ehGD1i0digNF7Jy6MEyZ4oqeKsUTiC8QOtW0KUgPQGdiVWCMFsLYlQ--C6tHdLWxWqdQQD7Skektd7mbKfJ2xg86ob-E73z_iFXBWn4ArC-w0o1yW9Mz8ZwneMfzqOgehPoe1PLaQb7C34woPKRODgSoAlQL9JQl4oVB5VzIN6KG8T6XLabShm5mRjLzQGSrwbXiKCV5GB0bBMwoA3QLOITH2CiaEbQLPMwwqUyRDoe66KtFAHoKR8SMLFyiMhAaD7e2jEaUOy_dOvwATqtOUSGexDM0x-jDYuSDbor0ucQj6bdS58TTlQBYecKaUeh6YWuScTfr03KXNszkTbtdSIB2l_K9iM2l8W8iCdOFOaSMZhggJaBZLblb2gNYUD2taE9i9MjbeTdI0UcF6ht8AtIEEQ4DT0KrbEq9_6bTzE8tYtq2OMgdJOuXvwFRGfIFDMvKa_QcU8Buy4560NTITv059PrJ6VQYHoVV-bRHKdtsJnyukUkHBRE9j4kj0kSUYHyNhUoUxNkIuHdl3Pr0z-BZ4jU--QZ1jyWzRfNYud9IiEh6DfQU-FKN06WxPmbkuPJ5Fi4VbjSZjOIWU1fZa2C7ixEf-GaxFl3o8VMsw9g_SkXvU9T1ZsduK_NuIGkeOXCdvtm4t63tMNcBh6X3Xu10_rEfh__E7Tc-MOyrxGl43jyUDgbzHdYwzHaYOPQ77OTOndFM8QGmRC1OG48iJSZMvNV_F4BO3VJRXSUcwPWSqCRyYF-LYCLmfLqa3fv'  # Substitua pelo seu Access Token
LOCAL_DB_PATH = 'db.sqlite3'  # Caminho onde o banco será salvo localmente
DROPBOX_PATH = '/db.sqlite3'  # Caminho do banco no Dropbox

# Inicializa o cliente Dropbox
dbx = dropbox.Dropbox(ACCESS_TOKEN)

# Função para baixar o banco
def download_db():
    try:
        metadata, response = dbx.files_download(DROPBOX_PATH)
        with open(LOCAL_DB_PATH, 'wb') as f:
            f.write(response.content)
        print(f"Banco de dados baixado de {DROPBOX_PATH} com sucesso!")
    except Exception as e:
        print(f"Erro ao baixar o banco: {e}")

# Executa o download
if __name__ == '__main__':
    download_db()