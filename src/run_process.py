from task import decoder,mail

if __name__ == '__main__':
    total_slots = dict()
    total_slots["Tempo Rubato"] = decoder.Tempo_Rubato()

    mail.SendMail(total_slots)