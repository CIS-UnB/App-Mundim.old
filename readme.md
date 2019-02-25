Execução mobile:
"buildozer android debug deploy run logcat"
1. buildozer: builda o pacote
2. android: not ios
3. debug: not release
4. deploy: além de buildar, manda pro cel
5. run: além de mandar pro cel, executa o app
6. logcat: monitora o cel por mensagens do python
O buildozer não é instalado junto com o kivy, mas a instalação é bem straightforward

Execução não-mobile:
"python2 -m screen:onex,portrait,scale=0.75"
1. onex: celular teste; eu mesmo uso s8
2. portrait: not landscape
3. scale: escala da resolução; a maioria das telas não tem 1920px de altura, então escala acaba sendo útil
Tem como escolher telas de outras dimensões (tipo a do s8, que é 2960x1440). O s8 não tá na lista oficial de telas disponíveis, então eu editei o arquivo do kivy em kivy/modules/screen. Vai pedir DPI da tela e uma "razão de qualidade", tipo xxhd. Os dois tem no google.dev pra qualquer cel android.

Notas: por motivos de sistema operacional e como eles lidam com coisas gráficas (tipo o que fazer se você tiver uma linha com 1.5px de altura), qualquer implementação de design mobile fica ruim em sistemas não-mobile. Tem que dar uma abstraída na feiura e confiar que vai ficar igual o design oficial, e vai mesmo.

Abraços,
