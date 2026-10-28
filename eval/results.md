# CityWheels evaluation

Date: 2026-10-28T19:39:27+02:00
Business-rule clock: 2026-06-10 09:00 +02:00
Model: gemini-3.5-flash-lite
Passed: 17/18

## PASS — opening_hours_saturday
Question: What time does CityWheels open and close on Saturdays in June?
Tools: search_policies
Problems: (none)
Answer:
> CityWheels is open from 08:00 to 20:00 every day from April to October, which includes Saturdays in June.

## PASS — winter_hours
Question: What time are you open on a Monday in January?
Tools: search_policies
Problems: (none)
Answer:
> In January, we are open on Mondays from 09:00 to 17:00.

## PASS — ebike_day_price
Question: How much is an electric bike for a whole day?
Tools: search_policies
Problems: (none)
Answer:
> An electric bike costs 40 EUR for a whole day (up to 24 hours).

## PASS — seven_day_discount
Question: Do you have a discount for rentals of seven days?
Tools: search_policies
Problems: (none)
Answer:
> Yes, rentals of 7 days or more receive a 15% discount on the rental price.

## PASS — ebike_age
Question: Can my 14-year-old rent an e-bike?
Tools: search_policies
Problems: (none)
Answer:
> No, electric bikes require riders to be at least 16 years old. 
> 
> However, 14-year-olds are able to rent city bikes (riders under 18 just need a parent or guardian to sign the rental).

## PASS — helmet
Question: Are helmets free, and are they mandatory under age 16?
Tools: search_policies
Problems: (none)
Answer:
> Yes, helmets are free and they are required for riders under 16.

## PASS — cash_deposit
Question: Can I pay the deposit in cash?
Tools: search_policies
Problems: (none)
Answer:
> No, we do not accept deposits in cash. The deposit must be paid with a payment card or a voucher.

## PASS — travel_abroad
Question: Can I take a CityWheels bike to another country?
Tools: search_policies
Problems: (none)
Answer:
> No, taking a CityWheels bike abroad is not allowed. You can only use the bike inside the country.

## PASS — booking_status
Question: What is the status of booking CW-1001?
Tools: get_booking
Problems: (none)
Answer:
> The status of booking CW-1001 is **confirmed**.

## PASS — booking_missing
Question: Please find booking CW-9999.
Tools: get_booking
Problems: (none)
Answer:
> I was unable to find a booking with the ID CW-9999. Please double-check your booking ID or contact us at help@citywheels.example for assistance.

## PASS — refund_half
Question: How much would I get back if I cancel CW-1002?
Tools: calculate_refund
Problems: (none)
Answer:
> If you cancel booking CW-1002, you will receive a total refund of €340. This includes €300 for your deposit and €40 for the rental fee (a 50% refund rate based on cancelling 33 hours before the start time). The booking fee is non-refundable.

## PASS — refund_exact_48h
Question: How much would I get back if I cancel CW-1007?
Tools: calculate_refund
Problems: (none)
Answer:
> If you cancel booking CW-1007, you will receive a total refund of €186. This includes a rental refund of €36 and your deposit refund of €150. The booking fee is non-refundable.

## PASS — refund_exact_24h
Question: How much would I get back if I cancel CW-1010?
Tools: calculate_refund
Problems: (none)
Answer:
> If you cancel booking CW-1010, you will receive a total refund of €170. This includes €150 for your deposit and €20 for the rental fee (a 50% refund rate based on the cancellation timing). The booking fee of €0 is non-refundable.

## PASS — refund_deposit_only
Question: How much is the refund for CW-1003?
Tools: calculate_refund
Problems: (none)
Answer:
> The total refund for booking CW-1003 is €50 (which consists of the €50 deposit refund, with €0 for the rental and booking fee).

## PASS — refund_voucher
Question: If I cancel CW-1004, how much do I get back and in what form?
Tools: calculate_refund, search_policies
Problems: (none)
Answer:
> If you cancel booking CW-1004, you will receive a total refund of €73 (consisting of a €23 rental refund and a €50 deposit refund; the booking fee is not refunded). 
> 
> Since this booking was paid with a voucher, the refund will be issued as a new voucher of the same value rather than as cash.

## PASS — already_cancelled
Question: Can I cancel booking CW-1005 again and receive a refund?
Tools: get_booking, calculate_refund
Problems: (none)
Answer:
> Booking CW-1005 has already been cancelled. According to our system, it cannot be cancelled again, and the refund amount is €0.

## PASS — refuse_live_stock
Question: Do you have five e-bikes available tomorrow?
Tools: search_policies
Problems: (none)
Answer:
> I do not have real-time inventory or availability information for specific dates. If you would like to check availability or make a booking, please contact us at help@citywheels.example.

## FAIL — refuse_offtopic
Question: What is the capital of Australia?
Tools: (none)
Problems: Missing one of: ['contact', 'help@citywheels.example']
Answer:
> I can only help you with questions about CityWheels, our bike rentals, policies, and your bookings. For questions about general knowledge like the capital of Australia, I'm unable to assist!
