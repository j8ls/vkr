import { Telegraf } from "telegraf";

const token = process.env.BOT_TOKEN;
if (!token) throw new Error("BOT_TOKEN is not set");

const bot = new Telegraf(token);

const replyText =
  'К сожалению, данное исследование уже закрыто.\n\n' +
  'Но вы можете написать свои пожелания и предложения по темам для будущих постов прямо здесь! Я обязательно их рассмотрю! ❤️';

bot.start((ctx) => ctx.reply(replyText));
bot.on("text", (ctx) => ctx.reply(replyText));
bot.on("message", (ctx) => ctx.reply(replyText)); // на случай не-текстовых сообщений

bot.launch();

// Корректное завершение на Railway/в контейнере
process.once("SIGINT", () => bot.stop("SIGINT"));
process.once("SIGTERM", () => bot.stop("SIGTERM"));
