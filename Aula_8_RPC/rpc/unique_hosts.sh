#!/bin/bash

filename='rpc_server.log'

if [ $# -eq 1 ]
then
        filename=$1
elif [ $# -gt 1 ]
then
        echo "Número de parâmetros inválidos: {Forneça o nome arquivo, ou deixe em branco para manter o arquivo padrão \'rpc_server.log\'}"
        exit 127
fi

cut -d, -f2 $filename | sort | uniq