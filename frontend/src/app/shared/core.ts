

export function olderThanWeekAgo(sale_date: Date) {
    const dateWeekAgo = new Date();
    dateWeekAgo.setDate(dateWeekAgo.getDate()-7);
    const saleDate = new Date(sale_date);

    return saleDate < dateWeekAgo;
}

export function olderThanDayAgo(sale_date: Date) {
    const dateDayAgo = new Date();
    dateDayAgo.setDate(dateDayAgo.getDate()-1);
    const saleDate = new Date(sale_date);

    return saleDate < dateDayAgo;
}


