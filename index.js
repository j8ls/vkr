import { Telegraf } from "telegraf";

const token = process.env.BOT_TOKEN;
if (!token) throw new Error("BOT_TOKEN is not set");

const adminChatId = process.env.ADMIN_CHAT_ID; // ваш chat id в Telegram
if (!adminChatId) console.warn("ADMIN_CHAT_ID is not set");

const bot = new Telegraf(token);

const replyText =
  'К сожалению, данное исследование уже закрыто.\n\n' +
  'Но вы можете написать свои пожелания и предложения по темам для будущих постов прямо здесь! Я обязательно их рассмотрю! ❤️';

bot.start(async (ctx) => {
  // Ответ пользователю
  await ctx.reply(replyText);

  // Уведомление вам (опционально)
  if (adminChatId) {
    await ctx.telegram.sendMessage(
      adminChatId,
      `Новый /start от пользователя: ${ctx.from?.first_name ?? ""} @${ctx.from?.username ?? "(no username)"} (id ${ctx.from?.id})`
    );
  }
});

bot.on("message", async (ctx) => {
  // 1) Забираем, что прислали
  const from = ctx.from;
  const text = ctx.message?.text;
  const caption = ctx.message?.caption;

  const body =
    text ? text :
    caption ? `[media] ${caption}` :
    `[не текст] type: ${ctx.updateType}`;

  // 2) Пересылаем вам текстом
  if (adminChatId) {
    await ctx.telegram.sendMessage(
      adminChatId,
      `Пожелание/сообщение:\n${body}\n\nОт: ${from?.first_name ?? ""} ${from?.last_name ?? ""}\nUsername: ${from?.username ? "@" + from.username : "(нет)"}\nid: ${from?.id}`
    );
  }

  // 3) Отвечаем пользователю вашим шаблоном
  await ctx.reply(replyText);
});

bot.launch();

process.once("SIGINT", () => bot.stop("SIGINT"));
process.once("SIGTERM", () => bot.stop("SIGTERM"));
