from .base_email import header 
from utility.variables import projectName
class EmailTemplates():
    
    def __init__(self,data):
        self.data = data
        self.html_content = header(data['username'])

    def register(self):
        data = self.data
        html_content = self.html_content

        html_content+= f'text-align:left;line-height: 18px; padding:1em;"><span> Welcome to {projectName} </span>!<br><br>'   
        html_content+= f'<span> Please click the link to verify your {projectName} Account </span><br><br>'   
        html_content+= '<span>' + data['link'] + '</span><br><br></td></tr>'
              
        return html_content
    
    def forget_password(self):
        data = self.data
        html_content = self.html_content

        html_content+= f'text-align:left;line-height: 18px; padding:1em;"><span> Thanks for using {projectName} </span>!<br><br>'   
        html_content+= f'<span> Please click the link below to reset your {projectName} account password </span><br><br>'   
        html_content+= '<span>' + data['link'] + '</span><br><br></td></tr>'
              
        return html_content