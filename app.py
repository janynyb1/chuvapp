from flask import Flask, render_template, request, jsonify
from data_processing import read_posto_data, read_all_posto_data, obter_dados_do_grafico1, obter_dados_do_grafico2, obter_dados_do_grafico3
import pandas as pd

app = Flask(__name__)

postos_pluviometricos = {
    '80': {'latitude': -6.76, 'longitude': -38.96, 'dados': {'2023': {'1': 10, '2': 15, '3': 20}}},
    '133': {'latitude': -3.67, 'longitude': -38.97, 'dados': {'2023': {'1': 5, '2': 8, '3': 12}}},
    '349': {'latitude': -5.91, 'longitude': -39.26, 'dados': {'2023': {'1': 7, '2': 10, '3': 18}}}
}

@app.route('/')
def index():
    df_posto_80 = read_posto_data('80')
    all_posto_data = read_all_posto_data()

    return render_template('index.html', data_posto_80=df_posto_80, all_posto_data=all_posto_data)


@app.route('/grafico')
def grafico():
    dados_grafico1 = obter_dados_do_grafico1() 
    dados_grafico2 = obter_dados_do_grafico2() 
    dados_grafico3 = obter_dados_do_grafico3()  

    return jsonify(dados_grafico1=dados_grafico1, dados_grafico2=dados_grafico2, dados_grafico3=dados_grafico3)

@app.route('/map', methods=['GET'])
def map():
    ano = request.args.get('ano')
    mes = request.args.get('mes')
    
    
    postos = read_all_posto_data()
    
    if postos:
        return render_template('map.html', postos=postos, ano=ano, mes=mes)
    else:
        return "Erro ao carregar os dados dos postos pluviométricos", 500

@app.route('/postos')
def get_postos():
    return jsonify(postos_pluviometricos)

def ler_dados_posto_pluviometrico(file_path):
    
    df = pd.read_csv(file_path)
    
    return df


@app.route('/posto/<posto_id>')
def obter_dados_posto_pluviometrico(posto_id):
    file_path = f'posto/{posto_id}.csv'
    df = ler_dados_posto_pluviometrico(file_path)
    return jsonify(df.to_dict())

@app.route('/series-temporais')
def calcular_series_temporais():
    return jsonify({'mensagem': 'Séries temporais calculadas'})

if __name__ == '__main__':
    app.run(debug=True, port=500)


