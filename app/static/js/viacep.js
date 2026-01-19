/**
 * Script de autopreenchimento de endereço via CEP.
 * Fonte: ViaCEP (viacep.com.br)
 * Adaptado para o projeto Checkout Transparente
 */

function limpa_formulário_cep() {
            document.getElementById('logradouro').value=("");
            document.getElementById('bairro').value=("");
            document.getElementById('cidade').value=("");
            document.getElementById('estado').value=("");
    }

    function preencher_campo_endereco(conteudo) {
        if (!("erro" in conteudo)) {
            document.getElementById('logradouro').value=(conteudo.logradouro);
            document.getElementById('bairro').value=(conteudo.bairro);
            document.getElementById('cidade').value=(conteudo.localidade);
            document.getElementById('estado').value=(conteudo.estado);

            document.getElementById('numero').focus();
        }
        else {
            limpa_formulário_cep();
            alert("CEP não encontrado.");
        }
    }
        
    function pesquisacep(valor) {
        //Nova variável "cep" somente com dígitos.
        var cep = valor.replace(/\D/g, '');

        //Verifica se campo cep possui valor informado.
        if (cep != "") {

            //Expressão regular para validar o CEP.
            var validacep = /^[0-9]{8}$/;

            //Valida o formato do CEP.
            if(validacep.test(cep)) {

                //Preenche os campos com "..." enquanto consulta webservice.
                document.getElementById('logradouro').value="...";
                document.getElementById('bairro').value="...";
                document.getElementById('cidade').value="...";
                document.getElementById('estado').value="...";

                //Cria um elemento javascript.
                var script = document.createElement('script');

                //Sincroniza com o callback.
                script.src = 'https://viacep.com.br/ws/'+ cep + '/json/?callback=preencher_campo_endereco';

                //Insere script no documento e carrega o conteúdo.
                document.body.appendChild(script);

            }
            else {
                //cep é inválido.
                limpa_formulário_cep();
                alert("Formato de CEP inválido.");
            }
        }
        else {
            //cep sem valor, limpa formulário.
            limpa_formulário_cep();
        }
    };