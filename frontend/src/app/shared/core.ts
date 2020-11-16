export function olderThanWeekAgo(sale_date: Date) {
    const dateWeekAgo = new Date();
    dateWeekAgo.setDate(dateWeekAgo.getDate()-7);
    const saleDate = new Date(sale_date);

    return saleDate < dateWeekAgo
}