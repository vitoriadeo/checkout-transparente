# Checkout Transparente <sub>(em desenvolvimento)</sub>

Este é um projeto que demonstra a implementação completa de um checkout transparente utilizando a API de pagamentos do Asaas.

O objetivo é implementar uma solução de checkout transparente para a venda de um produto, servindo como aprendizado para novas tecnologias e consolidação de coisas que já sei. O sistema permitirá o pagamento (Boleto ou PIX) diretamente no site próprio, sem redirecionamento, integrando-se à API do Asaas em modo Sandbox para processamento e a um banco de dados para gestão de clientes e pedidos.

---

## Sobre o projeto

O projeto utiliza uma arquitetura monolítica em Python, com o Flask sendo responsável tanto pela lógica de back-end quanto pela renderização das páginas.

O fluxo de compra é dividido em três páginas:

1. **Página de Produto:** Exibe um produto fictício numa página simples. Nessa página há informações do produto, seletor de quantidade do produto, valor e um botão 'Comprar'.
2. **Página de Checkout:** Para onde o usuário é levado após adicionar ao carrinho. Exibe o resumo do pedido e o formulário para pagamento.
3. **Página de Pedido Confirmado:** Página de sucesso exibida após um pagamento ser aprovado.

---

## Documentação

A documentação pode ser encontrada na pasta `/docs`

* [Análise de requisitos](./docs/requisitos/)
* [Modelagem do banco de dados](./docs/modelagem/)
