using System;
using System.Collections.Generic;
using System.Linq;

public class Topping
{
    public string Name { get; set; }
    public decimal Price { get; set; }

    public Topping(string name, decimal price)
    {
        Name = name;
        Price = price;
    }
}



public class Pizza
{
    public string rozmiar { get; set; }
    public decimal cena_podst { get; set; }
    public List<Topping> Toppings { get; set; } = new List<Topping>();

    public Pizza(string size)
    {
        rozmiar = size;
        cena_podst = size switch
        {
            "M(mała)" => 20,
            "D(duża)" => 25,
            "W(wielka)" => 30,
            _ => 20
        };
    }

    public decimal GetTotalPrice()
    {
        return cena_podst + Toppings.Sum(t => t.Price);
    }

    public override string ToString()
    {
        string toppings = Toppings.Count > 0 ? string.Join(", ", Toppings.Select(t => t.Name)) : "brak";
        return $"Pizza {rozmiar}, dodatki: {toppings}, cena: {GetTotalPrice():C}";
    }
}



public class Order
{
    public List<Pizza> Pizze { get; set; } = new List<Pizza>();
    public string adres { get; set; }
    public int czasowka { get; set; }

    public decimal GetTotalOrderPrice()
    {
        return Pizze.Sum(p => p.GetTotalPrice());
    }

    public void PrintSummary()
    {
        Console.WriteLine("\n---- Podsumowanie zamówienia ----");
        foreach (var pizza in Pizze)
        {
            Console.WriteLine(pizza);
        }

        Console.WriteLine($"\nAdres dostawy: {adres}");
        Console.WriteLine($"Szacowany czas dostawy: {czasowka} minut");
        Console.WriteLine($"Razem do zapłaty: {GetTotalOrderPrice():C}");
    }
}



class pizza_cszarp_folc
{
    static void Main()
    {
        List<Topping> availableToppings = new List<Topping>
        {
            new Topping("Ser ", 3),
            new Topping("Szynka", 4),
            new Topping("Pieczarki", 2),
            new Topping("Oliwki", 2.5m),
            new Topping("Ananas", 3.5m)
        };

        Order order = new Order();

        bool addingPizza = true;//23

        while (addingPizza)
        {
            Console.Write("Wybierz rozmiar pizzy (M/D/W)    ");
            Console.Write("M = mała, D = duża, W = wielka: ");
            string size = Console.ReadLine().ToUpper();
            Pizza pizza = new Pizza(size);

            Console.WriteLine("Dostępne dodatki:");
            for (int i = 0; i < availableToppings.Count; i++)
            {
                Console.WriteLine($"{i + 1}. {availableToppings[i].Name} ({availableToppings[i].Price:C})");
            }

            Console.Write("Wybierz dodatki (np. 1,3,5): ");
            string[] selected = Console.ReadLine().Split(',');
            foreach (var s in selected)
            {
                if (int.TryParse(s.Trim(), out int index) && index > 0 && index <= availableToppings.Count)
                {
                    pizza.Toppings.Add(availableToppings[index - 1]);
                }
            }

            order.Pizze.Add(pizza);

            Console.Write("Czy chcesz dodać kolejną pizzę? (T/N): ");
            addingPizza = Console.ReadLine().Trim().ToUpper() == "T";
        }

        Console.Write("\nPodaj adres dostaawy: "); 
        order.adres = Console.ReadLine();

        Random rand = new Random();
        order.czasowka = rand.Next(60, 121);

        order.PrintSummary();
    }
}
