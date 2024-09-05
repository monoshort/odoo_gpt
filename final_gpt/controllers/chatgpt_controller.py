from odoo import http
from odoo.http import request

class ChatGPTController(http.Controller):

    @http.route('/chatgpt/send', type='json', auth='user')
    def send_message(self, message):
        if not message:
            return {'error': 'No message provided.'}

        try:
            # Maak een nieuw ChatGPT model record met het meegegeven bericht
            chatgpt_model = request.env['chatgpt.model'].sudo().create({'message': message})
            
            # Verstuur het bericht en haal de reactie op
            chatgpt_model.send_message()
            
            # Haal de laatste reactie op
            response = chatgpt_model.response_ids.sorted('create_date', reverse=True)
            if response:
                return {'response': response[0].response}
            else:
                return {'error': 'No response received from ChatGPT.'}

        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}
