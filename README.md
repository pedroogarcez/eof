<h1 align="center"> EOF Python Tutorial </h1>

<p align="justify"> 
  A aplicação de Funções Ortogonais Empíricas (EOF, do inglês Empirical Orthogonal Functions) é uma técnica estatística utilizada para analisar e decompor a variabilidade espacial de um conjunto de dados. Através do reconhecimento dos padrões dominantes presentes nas variáveis analisadas, é possível identificar diferentes padrões em cada modo calculado. Nos modelos deste exemplos, primeiramente vamos preparar o arquivo de entrada através de comandos com <i> Climate Data Operators </i>. Dentre as bibliotecas que compõem a linguagem de programação Python, vamos utilizar a <i> eofs </i> para calcular os modos normais.
  
 <h2> 1. Utilizando os CDO: </h2>
 <p align="justify"> Primeiramente, vamos utilizar os comandos do CDO para determinar as características do arquivo que iremos analisar. Neste exemplo, os dados serão referentes a altura Geopotencial (m) para analisar seu comportamento no intervalo de Dezembro a Fevereiro no Hemisfério Sul </p>
 <p>
Selecionando os meses de Dezembro, Janeiro e Fevereiro e as coordenadas do Hemisfério Sul:
</p>
  
``` bash
  cdo select,month=12,1,2,lonlatbox=0,360,-90,0 nome_arquivo_entrada.nc nome_arquivo_saida.nc
  
```
  
  
  <h2> Referências </h2>
   
