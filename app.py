from flask import Flask, Response
import subprocess
import html

app = Flask(__name__)

@app.route('/')
def stream_log():
    def generate():
        process = subprocess.Popen(
            ['tail', '-n', '40', '-f', '/home/user/log.log'], #ultimas 40 linhas
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        yield """<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Log do Bot</title>
<style>
* { 
    margin: 0; 
    padding: 0; 
    box-sizing: border-box; 
}
body { 
    background: #000; 
    color: #FF69B4; 
    font-family: 'Courier New', Courier, monospace; 
    height: 100vh; 
    overflow: hidden; 
}
.container { 
    height: 100vh; 
    display: flex; 
    flex-direction: column; 
    padding: 10px; 
}
h3 { 
    text-align: center; 
    padding: 5px 0; 
    flex-shrink: 0; 
    font-size: 18px;
}
.log-container { 
    flex: 1; 
    overflow: auto; 
}
pre {
    white-space: pre;
    font-family: 'Courier New', Courier, monospace;
    line-height: 1;
    background: #000;
    color: #FF69B4;
    margin: 0;
    padding: 0;
    min-width: max-content;
}

/* FORÇAR LARGURA UNIFORME USANDO TABULAÇÃO */
.blank, .filled {
    display: inline-block;
}

/* ESTILOS PARA CELULAR */
@media (max-width: 768px) {
    .container {
        padding: 5px;
    }
    h3 {
        font-size: 14px;
        padding: 3px 0;
    }
    pre {
        font-size: 4.5px;
        letter-spacing: 0.3px;
    }
    .blank, .filled {
        width: 2.25px;
    }
}

/* ESTILOS PARA COMPUTADOR */
@media (min-width: 769px) {
    .container {
        padding: 15px;
    }
    h3 {
        font-size: 20px;
        padding: 10px 0;
    }
    pre {
        font-size: 12px;
        letter-spacing: 0.7px;
    }
    .blank, .filled {
        width: 7px;
    }
}

/* ESTILOS PARA TELAS MUITO GRANDES */
@media (min-width: 1200px) {
    pre {
        font-size: 14px;
    }
    .blank, .filled {
        width: 8px;
    }
}

/* Scrollbar personalizada */
.log-container::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

.log-container::-webkit-scrollbar-track {
    background: #000;
}

.log-container::-webkit-scrollbar-thumb {
    background: #FF69B4;
    border-radius: 4px;
}

.log-container::-webkit-scrollbar-thumb:hover {
    background: #ff85c1;
}
</style>
</head>
<body>
<div class="container">
<h3>LOG BOT</h3>
<div class="log-container"><pre>
"""
        
        for line in iter(process.stdout.readline, ''):
            # Substituir espaços por elementos com largura fixa
            processed_line = ""
            for char in line.rstrip('\n'):
                escaped_char = html.escape(char)
                if char == ' ':
                    processed_line += '<span class="blank">&nbsp;</span>'
                else:
                    processed_line += f'<span class="filled">{escaped_char}</span>'
            processed_line += '\n'
            yield processed_line
            
        yield "</pre></div></div></body></html>"

    return Response(generate(), mimetype='text/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
