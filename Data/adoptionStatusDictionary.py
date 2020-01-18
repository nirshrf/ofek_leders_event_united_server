from Entities import AdoptionStatus


adoption_status_dictionary = dict(adopted=AdoptionStatus(1, 1, 'ADOPTED'),
                                  not_adopted=AdoptionStatus(2, 2, 'NOT_ADOPTED'),
                                  confirmed_adopted=AdoptionStatus(3, 3, 'CONFIRMED_ADOPTED'),
                                  adoption_canceled=AdoptionStatus(4, 4, 'ADOPTION_CANCELED'))


def get_adoption_status(adoption_status):
    if adoption_status in adoption_status_dictionary.keys():
        return adoption_status_dictionary[adoption_status]
    raise KeyError

