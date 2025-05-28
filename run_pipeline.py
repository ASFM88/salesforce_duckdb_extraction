import subprocess
import sys
import time

PIPELINE_ETAPAS = [
    ("🔄 Executando RAW Builder", "raw_builder.py"),
    ("⚙️ Executando STAGE Builder", "stage_builder.py"),
    ("🚀 Executando TRUSTED Builder", "trusted_builder.py"),
    ("📤 Exportando para SQLite", "export_sqlite.py")
]

def rodar_etapa(nome, script):
    print(f"\n{nome}")
    inicio = time.time()
    try:
        subprocess.run([sys.executable, script], check=True)
        print(f"✅ {script} finalizado em {round(time.time() - inicio, 2)}s")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar {script}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🧠 Iniciando pipeline de dados Salesforce → DuckDB + SQLite")
    for nome, script in PIPELINE_ETAPAS:
        rodar_etapa(nome, script)
    print("\n🏁 Pipeline concluído com sucesso!")
