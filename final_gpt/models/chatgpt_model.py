from odoo import models, fields, api, _
import openai
import logging

_logger = logging.getLogger(__name__)

class ChatGPTModel(models.Model):
    _name = 'chatgpt.model'
    _description = 'ChatGPT Model'

    name = fields.Char(string='Name')
    message = fields.Text(string='Message')
    response_ids = fields.One2many('chatgpt.message', 'chatgpt_id', string='Responses')

    @api.model
    def create(self, vals_list):
        """Override create to handle batch processing."""
        records = super(ChatGPTModel, self).create(vals_list)
        # Add any custom logic here if needed
        return records

    def send_message(self):
        if not self.message:
            _logger.warning("No message provided.")
            return

        # Haal de API-sleutel op uit de omgevingsvariabelen
        api_key = ''
        if not api_key:
            _logger.error("API key not found.")
            return

        # Stel de API-sleutel in voor OpenAI
        openai.api_key = api_key

        # Haal facturen op uit Odoo
        invoice_info = self.get_invoice_info()

        # Voorbereiden van het chatverhaal
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        
        if invoice_info:
            messages.append({"role": "system", "content": f"Here is the invoice information:\n{invoice_info}"})
        
        # Voeg voorgaande chatgeschiedenis toe
        for response in self.response_ids:
            messages.append({"role": "user", "content": response.message})

        # Voeg het nieuwe gebruikersbericht toe
        messages.append({"role": "user", "content": self.message})

        try:
            # Verstuur het bericht naar OpenAI en ontvang de reactie
            chat_completion = openai.ChatCompletion.create(
                model="gpt-4",  # Gebruik bijvoorbeeld "gpt-4" of "gpt-3.5-turbo"
                messages=messages
            )

            # Haal de gegenereerde content op van de API-reactie
            bot_response = chat_completion.choices[0].message['content']

            # Voeg het nieuwe antwoord toe aan de chatgeschiedenis
            self.env['chatgpt.message'].create({
                'chatgpt_id': self.id,
                'message': self.message,
                'response': bot_response
            })
            _logger.error(invoice_info)

        except Exception as e:
            _logger.error(f"OpenAI error: {str(e)}")

    def get_invoice_info(self):
        """Haalt factuurinformatie op uit Odoo en retourneert als string."""
        try:
            # Zoek alle openstaande facturen
            invoice_model = self.env['account.move']
            invoices = invoice_model.search([('move_type', '=', 'out_invoice'), ('state', '=', 'posted')])
            
            if not invoices:
                return "No invoices found."

            # Verzamel factuurinformatie
            invoice_info_list = []
            for invoice in invoices:
                invoice_info_list.append(
                    f"Factuur ID: {invoice.id}\n"
                    f"Factuurnummer: {invoice.name}\n"
                    f"Datum: {invoice.invoice_date}\n"
                    f"Klantennaam: {invoice.partner_id.name}\n"
                    f"Bedrag: {invoice.amount_total}"
                )
            
            return "\n\n".join(invoice_info_list)
        
        except Exception as e:
            _logger.error(f"Error retrieving invoices: {str(e)}")
            return "Error retrieving invoices."


class ChatGPTMessage(models.Model):
    _name = 'chatgpt.message'
    _description = 'ChatGPT Message'

    chatgpt_id = fields.Many2one('chatgpt.model', string='ChatGPT')
    message = fields.Text(string='Message')
    response = fields.Text(string='Response')

    @api.model
    def create(self, vals_list):
        """Override create to handle batch processing."""
        records = super(ChatGPTMessage, self).create(vals_list)
        return records
