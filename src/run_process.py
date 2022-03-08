from task import decoder,mail

if __name__ == '__main__':
    total_slots = dict()
    total_slots["Decoder"]["Tempo Rubato"] = decoder.Tempo_Rubato()
    print(total_slots)
    # mail.SendMail(total_slots)