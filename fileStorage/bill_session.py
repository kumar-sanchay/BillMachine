from django.conf import settings


class BillSession:
    """
    Session For Bill
    """
    def __init__(self, request):
        self.session = request.session
        bill = self.session.get(settings.BILL_SESSION_ID)
        if not bill:
            bill = self.session[settings.BILL_SESSION_ID] = {}
        self.bill = bill

    def add(self, invoice_no, sr, data):
        """
        For adding the bill details
        :param invoice_no:
        :param data:
        :return:
        """
        self.bill[invoice_no][sr] = data
        self.save()

    def save(self):
        """
        saving the session
        :return:
        """
        self.session.modified = True

    def remove(self, invoice_no):
        """
        Removing the invoice from the bill
        :param invoice_no:
        :return:
        """
        if invoice_no in self.bill:
            del self.bill[invoice_no]
            self.save()
